


export default function Home(){
    return (
        <div className="page page-home">
            <header className="page-header">
                <h1 className="page-title">Zgrany budzet - system zarządzania budzetem państwowym</h1>
                <p className="page-intro">
                    To narzędzie wspiera urzędników w analizie, planowaniu i monitorowaniu wydatków publicznych
                    oraz ułatwia przygotowanie raportów budzetowych
                </p>
            </header>
            <section className="card-grid">
                <article className="card">
                    <h2 className="card-title">Transparentność finansów</h2>
                    <p className="card-text">
                        System zbiera dane z róznych jednostek i prezentuje je w czytelnej formie.
                        Ułatwia śledzenie realizacji budzetu oraz wykrywanie nieprawidłowości.
                    </p>
                </article>
                <article className="card">
                    <h2 className="card-title">Wsparcie decyzyjne</h2>
                    <p className="card-text">
                        Zaawansowane zestawienie i raporty pomagają w podejmowaniu decyzji dotyczących
                        podziału środków, korekt budzetowych oraz planowania kolejnych okresów.
                    </p>
                </article>
                <article className="card">
                    <h2 className="card-title">Bezpieczeństwo danych</h2>
                    <p className="card-text">
                        Dostęp do systemu jest ograniczony do uprawnionych uzytkowników,
                        a dane są przechowywane zgodnie z obowiązującymi przepisami prawa.
                    </p>
                </article>
            </section>
        </div>
    );
}