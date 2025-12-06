//panel do logowania
import '../../css/login.css'

export default function LoginPanel({onClose}) {
    const handleSubmit = (e) => {
        e.preventDefault(); //for later backend login
    };
    return (
        <div className="modal-backdrop" onClick={onClose}>
            <div className="modal" onClick={(e) => e.stopPropagation()}>
                <button className="modal-close" type="button" onClick={onClose}>
                    x
                </button>
                <h2>Zaloguj się</h2>
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