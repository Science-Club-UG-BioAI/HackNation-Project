//panel do logowania
import '../../css/login.css'
import { useState } from "react";

export default function LoginPanel({onClose, onLogin}) {
    const [error, setError] = useState(null);
    const handleSubmit = async (e) => {
        e.preventDefault(); 
        const formData = new FormData(e.target);
        const login = formData.get('login'); //placeholder
        const password = formData.get('password'); //placeholder
        
        try {
            const response = await fetch("http://localhost:8000/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({login, password}),
            });
            if (!response.ok) {
                const data = await response.json();
                setError(data.detail || "Niepoprawne dane logowania");
                return;
            }
            const data = await response.json();
            onLogin({login:data.login});
        } catch (err) {
            setError("Błąd połączenia z serwerem!!!");
        }
    };
    return (
        <div className="modal-backdrop" onClick={onClose}>
            <div className="modal" onClick={(e) => e.stopPropagation()}>
                <button className="modal-close" type="button" onClick={onClose}>
                    :D
                </button>
                <h2>Zaloguj się</h2>
                {error && <p className='error-msg'>{error}</p>}
                <form className="modal-form" onSubmit={handleSubmit}>
                    <label>
                        Login
                        <input type="text" name="login" required/>
                    </label>
                    <label>
                        Hasło
                        <input type="password" name="password" required/>
                    </label>
                    <button type="submit">Zaloguj</button>
                </form>
            </div>
        </div>
    );
}