import { useEffect, useState } from "react";

export default function useAuth() {
    const [isLoggedin, setIsLoggedIn] = useState(false)

    useEffect ( () => {
        const token = localStorage.getItem("access-token");
        setIsLoggedIn(!!token);
    }, [])

    return isLoggedin;
}