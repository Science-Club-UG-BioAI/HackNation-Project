import '../../css/topbar.css'

//uklad topbara
export default function Topbar({changeTab}){
    return (
        <section className="topbar">
            <div className='topbar-left'>
                <div className="topbar-logo">
                    <div className="logo-image">
                        <div className="logo-text">
                            <span className="logo-subtitle">Zgrany budżet</span>
                        </div>
                    </div>
                </div>
            </div>
            <div className='topbar-right'>
                <nav className="topbar-nav">
                    <button onClick={() => changeTab('home')}>Home</button>
                    <button onClick={() => changeTab('upload')}>Upload</button>
                </nav>
            </div>
            <hr className="topbar-line"></hr>
        </section>
    );
}
