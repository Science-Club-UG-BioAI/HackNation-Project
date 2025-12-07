

export default function BudgetAddData() {
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Add data – placeholder");
  };

  return (
    <div className="budget-section">
      <h2 className="budget-section-title">Dodanie danych do bazy</h2>
      <p className="budget-section-desc">
        Wypełnij formularz, aby dodać nowy rekord budżetowy do bazy danych.
      </p>

      <form className="form-grid" onSubmit={handleSubmit}>
        <div className="form-field">
          <label className="form-label">Rok budżetowy</label>
          <input
            type="number"
            className="form-input"
            placeholder="np. 2025"
          />
        </div>

        <div className="form-field">
          <label className="form-label">Jednostka / dział</label>
          <input
            type="text"
            className="form-input"
            placeholder="np. Wydział Edukacji"
          />
        </div>

        <div className="form-field">
          <label className="form-label">Kwota</label>
          <input
            type="number"
            className="form-input"
            placeholder="np. 150000"
          />
        </div>

        <div className="form-field form-field-full">
          <label className="form-label">Opis / uwagi</label>
          <textarea
            className="form-input form-textarea"
            placeholder="Krótki opis przeznaczenia środków…"
            rows={3}
          ></textarea>
        </div>

        <div className="form-actions">
          <button type="submit" className="btn-primary">
            Zapisz rekord w bazie
          </button>
        </div>
      </form>

      <div className="budget-info-placeholder">
        <p className="budget-info-text">
          afirmacja dodania :)
        </p>
      </div>
    </div>
  );
}

