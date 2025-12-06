import { useState } from "react"
import Home from "./pages/home";
import Upload from "./pages/upload"
import Topbar from "./pages/main_components/topbar";

function App() {
    const [activeTab, setActiveTab] = useState('home');

    return (
        <div className="app">
            <Topbar changeTab={setActiveTab}/>
            <main>
                {activeTab === 'home' && <Home/>}
                {activeTab === 'upload' && <Upload/>}
            </main>
        </div>
    );
}
export default App;