import { useState } from "react"
import Home from "./pages/home";
import Upload from "./pages/system"
import Help from "./pages/help";
import Topbar from "./pages/main_components/topbar";
import LoginPanel from "./pages/main_components/login";

function App() {
    const [activeTab, setActiveTab] = useState('home');
    const [isLoginOpen, setIsLoginOpen] = useState(false);

    return (
        <div className="app">
            <Topbar changeTab={setActiveTab}
                onOpenLogin={() => setIsLoginOpen(true)}
            />
            <main>
                {activeTab === 'home' && <Home/>}
                {activeTab === 'upload' && <Upload/>}
                {activeTab === 'help' && <Help/>}
            </main>
            {isLoginOpen && (
        <LoginPanel onClose={() => setIsLoginOpen(false)} />)}
        </div>
    );
}
export default App;