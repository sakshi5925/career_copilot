import {createSlice , createAsyncThunk} from  "@reduxjs/toolkit"
import { authService } from "./authService"

export const registerUser=createAsyncThunk(
    "auth/register",
    async (userData,{rejectWithValue})=>{
        try{
            return await authService.register(userData);
        }
        catch(error){
            return rejectWithValue(
                error.response?.data?.detail || "Registration failed"
            );       
        }
    })


export const loginUser=createAsyncThunk(
    "auth/login",
    async(credential,{rejectWithValue})=>{
        try{
            return await authService.login(credential);
        }
        catch(error){
            return rejectWithValue(
                error.response?.data?.detail || "Login failed"
            );
        }
    }
);


const  authSlice =createSlice({
    name:"auth",

    initialState:{
        user:null,
        token: localStorage.getItem("access_token"),
        loading: false,
        error: null
    },

    reducers:{
        logout :(state)=>{
            state.user=null;
            state.token=null;
            state.loading=false;
            state.error=null;
            localStorage.removeItem("access_token")
        },
        clearAuthError:(state)=>{
            state.error=null;
        },
    },
    
    extraReducers:(builder)=>{
        builder
            // register
            .addCase(registerUser.pending,(state)=>{
                state.loading=true;
                state.error=null;
            })
            .addCase(registerUser.fulfilled,(state)=>{
                state.loading=false;
            })
            .addCase(registerUser.rejected,(state,action)=>{
                state.loading =false;
                state.error=action.payload;
            })
            
            //login

            .addCase(loginUser.pending, (state)=>{
                state.loading=true;
                state.error=null;
            })
            .addCase(loginUser.fulfilled,(state,action)=>{
                state.loading=false;
                state.token = action.payload.access_token;
                localStorage.setItem("access_token",action.payload.access_token);
            })
            .addCase(loginUser.rejected,(state,action)=>{
                state.loading =false;
                state.error=action.payload;
            });
    },
});

export const {logout,clearAuthError} = authSlice.actions

export default authSlice.reducer;