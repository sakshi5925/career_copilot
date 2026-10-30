import os
import json
from pydantic import ValidationError
from app.ai.exceptions import AIServiceError
from dotenv import load_dotenv
from groq import Groq

from app.ai.schemas import ResumeAnalysis
from app.job_analysis.schemas import JobAnalysisResult
from app.matching.schemas import JobMatchResult
import re


load_dotenv()


class AIService:

    def __init__(self):
        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )


    def clean_resume_answer(self, answer: str) -> str:
        
        answer = re.sub(r"\*{1,3}(.*?)\*{1,3}", r"\1", answer)
        answer = re.sub(r"_{1,3}(.*?)_{1,3}", r"\1", answer)

        # Remove Markdown headings
        answer = re.sub(r"(?m)^\s{0,3}#{1,6}\s+", "", answer)

        # Remove bullet markers at the beginning of lines
        answer = re.sub(r"(?m)^\s*[-*+]\s+", "", answer)

        # Remove numbered list markers
        answer = re.sub(r"(?m)^\s*\d+[.)]\s+", "", answer)

        return answer.strip()

    def analyze_resume(self, resume_text: str):

        prompt = f"""
        You are an expert resume analyzer.

        Analyze the following resume.

        Return ONLY valid JSON.

        The JSON must have exactly these fields:

        {{
            "score": integer between 0 and 100,
            "strengths": list of strings,
            "weaknesses": list of strings,
            "missing_skills": list of strings,
            "recommendations": list of strings
        }}

        Do not return markdown.
        Do not return explanations outside the JSON.

        Resume:
        {resume_text}
        """
        try:
            response = self.client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert resume analyzer."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]         

            )
        
        except Exception as e:
            raise AIServiceError(
                "AI service is currently unavailable"
            ) from e

        response_text=response.choices[0].message.content

        try:
            data = json.loads(response_text)

        except json.JSONDecodeError:
            raise ValueError("AI returned invalid JSON")

        try:
            analysis = ResumeAnalysis(**data)

        except ValidationError:
            raise ValueError("AI returned invalid resume analysis")
       
        
        return  analysis



    def analyze_job(self, job_description: str):

        prompt = f"""
        You are an expert job description analyzer.

        Analyze the following job description.

        Return ONLY valid JSON.

        The JSON must have exactly these fields:

        {{
            "summary": "short summary of the job",
            "required_skills": ["skill1", "skill2"],
            "preferred_skills": ["skill1", "skill2"],
            "responsibilities": ["responsibility1", "responsibility2"],
            "experience_required": "required experience or null",
            "education_required": "required education or null"
        }}

        Rules:
        - required_skills = skills that are required for the job.
        - preferred_skills = nice-to-have skills.
        - responsibilities = main responsibilities of the role.
        - If experience is not mentioned, return null.
        - If education is not mentioned, return null.
        - Do not return markdown.
        - Do not return explanations outside the JSON.

        Job Description:
        {job_description}
        """

        try:
            response = self.client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert job description analyzer."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

        except Exception as e:
            raise AIServiceError(
                "AI service is currently unavailable"
            ) from e

        response_text = response.choices[0].message.content
        print("AI RESPONSE:")
        print(response_text)

        try:
            data = json.loads(response_text)

        except json.JSONDecodeError as e:
            raise ValueError(
                "AI returned invalid JSON"
            ) from e

        try:
            analysis = JobAnalysisResult(**data)

        except ValidationError as e:
            raise ValueError(
                "AI returned invalid job analysis"
            ) from e

        return analysis


    def match_resume_to_job(
        self,
        resume_text: str,
        job_description: str
    ):
        prompt = f"""
        You are an expert technical recruiter and resume-job matching system.

        Compare the candidate's resume with the job description.

        Return ONLY valid JSON.

        The JSON must have exactly these fields:

        {{
            "match_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "strengths": [],
            "weaknesses": [],
            "recommendation": ""
        }}

        Rules:

        - match_score must be a number between 0 and 100.
        - matched_skills = skills required by the job that the candidate clearly has.
        - missing_skills = important job skills that are missing from the resume.
        - strengths = reasons why the candidate is a good fit.
        - weaknesses = important gaps or weaknesses relative to the job.
        - recommendation = a short practical recommendation such as:
        "Strong match. Recommended to apply."
        - Do not invent skills that are not present in the resume.
        - Do not assume a skill just because it is related to another skill.
        - Base the comparison only on the provided resume and job description.
        - Do not return markdown.
        - Do not return explanations outside the JSON.

        CANDIDATE RESUME:
        {resume_text}

        JOB DESCRIPTION:
        {job_description}
        """

        try:
            response = self.client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert resume-job matching system."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
        except Exception as e:
            raise AIServiceError(
                "AI service is currently unavailable"
            ) from e

        response_text = response.choices[0].message.content

        print("AI MATCH RESPONSE:")
        print(response_text)

        try:
            data = json.loads(response_text)
        except json.JSONDecodeError as e:
            raise ValueError("AI returned invalid JSON") from e

        try:
            match = JobMatchResult(**data)
        except ValidationError as e:
            raise ValueError(
                "AI returned invalid job match"
            ) from e

        return match

    
    def generate_resume_answer(
        self,
        question: str,
        context: str,
        conversation_history: list[dict[str, str]] | None = None
    ) -> str:

        if not context or not context.strip():
            return "I couldn't find that information in your resume. Could you try asking something else?"

        messages = [
            {
                "role": "system",
                "content": """
    You are a friendly AI career assistant who talks naturally with users about their resumes.

    Your main goal is to answer questions like a helpful human would in a normal conversation, not like a report generator.

    STRICT RULES:

    1. Answer the user's question directly. Do not start with introductions like "Here's a quick rundown", "You've worked with a solid mix", or "Based on your resume".
    2. For simple questions, respond in one natural paragraph of 2–5 sentences.
    3. Do not use Markdown formatting. Never use **, __, #, headings, or decorative symbols.
    4. Do not use bullet points or numbered lists unless the user explicitly asks for them.
    5. When asked about a tech stack, explain the main technologies naturally in a sentence or short paragraph instead of creating categories and lists.
    6. Keep the response concise, relevant, and easy to read.
    7. Avoid repeating the same information or adding unnecessary conclusions.
    8. Use only facts supported by the supplied resume information. Never invent skills, experience, achievements, or metrics.
    9. If information is unavailable, say so honestly.
    10. For interview introduction questions, answer in the first person as if the candidate is speaking.
    11. Use conversation history to understand follow-up questions.
    12. Never mention internal processing, retrieved chunks, or sources.

    Before responding, check that your answer follows every formatting rule.
    """
            }
        ]

        if conversation_history:
            messages.extend(conversation_history[-6:])

        messages.append({
            "role": "user",
            "content": f"""
    Resume information:
    {context}

    User's question:
    {question}

    Answer naturally and directly, using the resume information above.
    """
        })

        try:
            response = self.client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=messages,
                temperature=0.4
            )

        except Exception as e:
            raise AIServiceError(
                "AI service is currently unavailable"
            ) from e

        answer = response.choices[0].message.content

        if not answer:
            raise AIServiceError("AI returned an empty response")

        return self.clean_resume_answer(answer)