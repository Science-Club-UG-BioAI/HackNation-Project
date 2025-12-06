import '../../css/topbar.css'

//uklad topbara
export default function Topbar({changeTab, onOpenLogin}){
    return (
        <section className="topbar">
            <div className="topbar-content">
                <div className="topbar-left">
                    <div className="topbar-logo">
                        <div className="logo-image">
                            <div className="logo-text">
                                <span className="logo-subtitle">Zgrany budżet</span>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="topbar-right">
                    <nav className="topbar-nav">
                        <button onClick={() => changeTab('home')}>Główna</button>
                        <button onClick={() => changeTab('upload')}>System</button>
                        <button onClick={() => changeTab('help')}>Pomoc</button>
                        <button onClick={onOpenLogin}>Zaloguj się</button>
                    </nav>
                </div>
            </div>
            <hr className="topbar-line" />
        </section>

    );
}
