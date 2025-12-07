

// ui/src/pages/BudgetExcel.jsx
export default function BudgetExcel() {
  const handleGenerate = (e) => {
    e.preventDefault();
    // TODO: wywołanie backendu do generowania Excela
    console.log("Generate Excel – placeholder");
  };

  return (
    <div className="budget-section">
      <h2 className="budget-section-title">Generowanie pliku Excel</h2>
      <p className="budget-section-desc">
        Wybierz zakres danych oraz kolumny, które mają znaleźć się w pliku.
      </p>

      <form className="form-grid" onSubmit={handleGenerate}>
        <div className="form-field">
          <label className="form-label">Zakres dat / lat</label>
          <input
            type="text"
            className="form-input"
            placeholder="np. 2023–2025"
          />
        </div>

        <div className="form-field">
          <label className="form-label">Filtr jednostki / działu</label>
          <input
            type="text"
            className="form-input"
            placeholder="np. Wydział Zdrowia"
          />
        </div>

        <div className="form-field form-field-full">
          <label className="form-label">Kolumny do uwzględnienia</label>
          <div className="form-checkbox-group">
            <label className="form-checkbox">
              <input type="checkbox" /> ID rekordu
            </label>
            <label className="form-checkbox">
              <input type="checkbox" /> Rok
            </label>
            <label className="form-checkbox">
              <input type="checkbox" /> Jednostka
            </label>
            <label className="form-checkbox">
              <input type="checkbox" /> Kwota
            </label>
            {/* TODO: realne kolumny z bazy */}
          </div>
        </div>

        <div className="form-actions">
          <button type="submit" className="btn-secondary">
            Generuj plik Excel
          </button>
        </div>
      </form>

      <div className="budget-download-placeholder">
        <p className="budget-download-title">Pobranie pliku (placeholder)</p>
        <button
          type="button"
          className="btn-primary"
          disabled
          title="Plik będzie dostępny po podłączeniu backendu"
        >
          Pobierz wygenerowany plik .xlsx
        </button>
      </div>
    </div>
  );
}
