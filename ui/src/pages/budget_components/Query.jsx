
export default function BudgetQuery() {
  const handleSubmit = (e) => {
    e.preventDefault();
    // TODO: wywołanie backendu (np. fetch do /api/query)
    console.log("Query submit – placeholder");
  };

  return (
    <div className="budget-section">
      <h2 className="budget-section-title">Sprawdzenie wartości w bazie</h2>
      <p className="budget-section-desc">
        Wpisz kryteria wyszukiwania, aby sprawdzić wartości w bazie danych.
      </p>

      <form className="form-grid" onSubmit={handleSubmit}>
        <div className="form-field">
          <label className="form-label">Kolumna / pole</label>
          <select className="form-input">
            <option value="">– wybierz –</option>
            <option value="id">ID rekordu</option>
            <option value="year">Rok budżetowy</option>
            <option value="department">Jednostka / dział</option>
            <option value="amount">Kwota</option>
            {/* TODO: podmienić na realne pola */}
          </select>
        </div>

        <div className="form-field">
          <label className="form-label">Wartość</label>
          <input
            type="text"
            className="form-input"
            placeholder="np. 2025, Wydział Finansów…"
          />
        </div>

        <div className="form-actions">
          <button type="submit" className="btn-primary">
            Szukaj w bazie
          </button>
        </div>
      </form>

      <div className="budget-results-placeholder">
        <p className="budget-results-title">Wyniki wyszukiwania (placeholder)</p>
        <div className="budget-results-table">
          <p>Tabela z rekordami</p>
        </div>
      </div>
    </div>
  );
}

