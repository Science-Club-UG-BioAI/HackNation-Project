//glowny panel zajmowania sie budzetem
import { useState } from "react"
import BudgetQuery from "./budget_components/Query"
import BudgetExcel from "./budget_components/Excel"
import BudgetAddData from "./budget_components/Insert"
import BudgetWord from "./budget_components/Word"
import '../css/budget.css'


const ACTIONS = {
    QUERY:"query",
    EXCEL:"excel",
    WORD:"word",
    ADD:"add",
};

export default function BudgetTool () {
    const [activeAction, setActiveAction] = useState(ACTIONS.QUERY);

    return (
        <div className="page page-budget">
            <header className="page-header page-header--budget">
                <h1 className="page-title">Narzedzie budzetowe</h1>
                <p className="page-intro">
                    Wybierz, co chcesz zrobić z danymi budzetowymi.
                </p>
            </header>
            <div className="budget-layout">
                <nav className="budget-sidebar" aria-label="Nawigacja narzędzia budzetowego">
                    <button 
                        type="button"
                        className={
                            `budget-sidebar-btn ${
                                activeAction === ACTIONS.QUERY ? "budget-sidebar-btn--active" : ""
                            }`
                        }
                        onClick={() => setActiveAction(ACTIONS.QUERY)}
                    >
                        1) Sprawdzenie danych w bazie
                    </button>
                    <button 
                        type="button"
                        className={
                            `budget-sidebar-btn ${
                                activeAction === ACTIONS.EXCEL ? "budget-sidebar-btn--active" : ""
                            }`
                        }
                        onClick={() => setActiveAction(ACTIONS.EXCEL)}
                    >
                        2) Wygenerowanie pliku Excel
                    </button>
                    <button 
                        type="button"
                        className={
                            `budget-sidebar-btn ${
                                activeAction === ACTIONS.WORD ? "budget-sidebar-btn--active" : ""
                            }`
                        }
                        onClick={() => setActiveAction(ACTIONS.WORD)}
                    >
                        3) Wygenerowanie pliku Word
                    </button>
                    <button 
                        type="button"
                        className={
                            `budget-sidebar-btn ${
                                activeAction === ACTIONS.ADD ? "budget-sidebar-btn--active" : ""
                            }`
                        }
                        onClick={() => setActiveAction(ACTIONS.ADD)}
                    >
                        4) Dodanie danych do bazy
                    </button>
                </nav>
                <section className="budget-main">
                    {activeAction === ACTIONS.QUERY && <BudgetQuery />}
                    {activeAction === ACTIONS.EXCEL && <BudgetExcel />}
                    {activeAction === ACTIONS.WORD && <BudgetWord />}
                    {activeAction === ACTIONS.ADD && <BudgetAddData />}
                </section>
            </div>
        </div>
    )




};
