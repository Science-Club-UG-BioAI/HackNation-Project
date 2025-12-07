
export default function BudgetWord() {
  const handleGenerate = (e) => {
    e.preventDefault();
    console.log("Generate Word – placeholder");
  };

  return (
    <div className="budget-section">
      <h2 className="budget-section-title">Generowanie pliku Word</h2>
      <p className="budget-section-desc">
        Wybierz konkretny wiersz (rekord) z bazy danych, z którego zostanie
        wygenerowany dokument.
      </p>

      <form className="form-grid" onSubmit={handleGenerate}>
        <div className="form-field">
          <label className="form-label">ID rekordu / numer sprawy</label>
          <input
            type="text"
            className="form-input"
            placeholder="np. 12345"
          />
        </div>

        <div className="form-field">
          <label className="form-label">Szablon dokumentu</label>
          <select className="form-input">
            <option value="">– wybierz –</option>
            <option value="summary">Zestawienie budżetowe</option>
            <option value="decision">Decyzja / postanowienie</option>
          </select>
        </div>

        <div className="form-actions">
          <button type="submit" className="btn-secondary">
            Generuj dokument Word
          </button>
        </div>
      </form>

      <div className="budget-download-placeholder">
        <p className="budget-download-title">Pobranie dokumentu (placeholder)</p>
        <button
          type="button"
          className="btn-primary"
          disabled
          title="Plik będzie dostępny po podłączeniu backendu"
        >
          Pobierz wygenerowany plik .docx
        </button>
      </div>
    </div>
  );
}
