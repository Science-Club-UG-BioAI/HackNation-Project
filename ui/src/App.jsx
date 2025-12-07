import { useState } from "react"
import Home from "./pages/home";
import System from "./pages/system"
import Help from "./pages/help";
import Topbar from "./pages/main_components/topbar";
import LoginPanel from "./pages/main_components/login";
import Footer from "./pages/main_components/footer";
import BudgetTool from "./pages/Budget_tool";
import HelpPrivate from "./pages/help_private";

function App() {
    const [activeTab, setActiveTab] = useState('home');
    const [isLoginOpen, setIsLoginOpen] = useState(false);
    //przygotowanie pod sprawdzanie zalogowania uzytkownika
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [user,setUser] = useState(null);
    //zapewnia logowanie
    const handleLogin = (userData) => {
        setUser(userData);
        setIsLoggedIn(true);
        setIsLoginOpen(false);
        setActiveTab('home')
    };
    //zapewnia wylogowywanaie
    const handleLogout = () => {
        setUser(null);
        setIsLoggedIn(false);
        setActiveTab('home')
    }

    return (
        <div className="app">
            <Topbar 
                changeTab={setActiveTab}
                onOpenLogin={() => setIsLoginOpen(true)}
                isLoggedIn={isLoggedIn}
                user={user}
                onLogout={handleLogout}
            />
            <main>
                {activeTab === 'home' && 
                    (!isLoggedIn? <Home/> : <BudgetTool/>
                )} 
                {activeTab === 'system' && <System/>}
                {activeTab === 'help' && 
                    (!isLoggedIn? <Help/> : <HelpPrivate/>)}
            </main>
            {isLoginOpen && (
        <LoginPanel onClose={() => setIsLoginOpen(false)} onLogin={handleLogin}/>)}
        <Footer/>
        </div>
    );
}
export default App;