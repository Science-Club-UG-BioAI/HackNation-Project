import { useState } from "react"
import Home from "./pages/home";
import Upload from "./pages/upload"

function App() {
    const [activeTab, setActiveTab] = useState('home');

    const renderTab = () => {
        switch (activeTab) {
            case 'home':
                return <Home />;
            case 'upload':
                return <Upload />;
            default:
                return <Home />;
        }
    };
    return (
        <div className="app">
            <nav className="topbar">
                <button onClick={() => setActiveTab('home')}>Home</button>
                <button onClick={() => setActiveTab('upload')}>Upload</button>
            </nav>
            <main className="content">
                {renderTab()}
            </main>
        </div>
    );
}
export default App;