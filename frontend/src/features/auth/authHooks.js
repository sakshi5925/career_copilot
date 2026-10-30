import { useAppDispatch, useAppSelector } from "@/app/hooks";
import { registerUser,loginUser,logout,clearAuthError } from "./authSlice";
import { selectCurrentUser, selectAuthToken,selectAuthLoading,selectAuthError } from "./authSelectors";

export function  useAuth(){
    const dispatch= useAppDispatch();
    const user=useAppSelector(selectCurrentUser);
    const token=useAppSelector(selectAuthToken);
    const loading =useAppSelector(selectAuthLoading);
    const error= useAppSelector(selectAuthError);


    return {
        user,
        token,
        loading,
        error,
        register : (userData) => dispatch(registerUser(userData)).unwrap(),
        login : (credential)=> dispatch(loginUser(credential)).unwrap(),
        logout :()=> dispatch(logout()),
        clearError: ()=> dispatch(clearAuthError()),

    };

}
