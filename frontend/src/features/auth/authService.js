import { apiClient } from "@/services/apiClient";

export const authService ={
    async register(userData){
        const response= await apiClient.post(
            "/auth/register",
            userData
        );
        return response.data;
    },

    async login(credentials){
        const formData= new URLSearchParams();

        formData.append("username",credentials.email);
        formData.append("password",credentials.password);

        const response=await apiClient.post(
            "/auth/login",
            formData
        );

        return response.data;
    },
}