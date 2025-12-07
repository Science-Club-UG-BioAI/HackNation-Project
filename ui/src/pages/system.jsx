import SystemTest from "./system_components/system-test";

export default function System(){
    return (
        <div className="page page-system">
            <header className="page-header">
                <h1 className="page-title">Jak działa system Zgrany budzet?</h1>
                <p className="page-intro">
                    Ponizszy opis przedstawia ogólną architekturę rozwiązania oraz podstawowe etapy pracy w systemie.
                </p>
            </header>
            <section className="card">
                <h2 className="card-title">Database</h2>
                <p className="card-text">
                    Tu wlozymy opis jak dziala przekazywanie danych itd
                </p>
                <p className="card-text">
                    Jakies moze schematy czy jakies role idk
                </p>
            </section>
        </div>
    );
}