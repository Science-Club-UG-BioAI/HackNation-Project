INSERT INTO ref.BudgetPart (PartCode, Name, IsGroup)
VALUES ('01', 'Kancelaria Prezydenta RP', 0);

INSERT INTO ref.Dzial (DzialCode, Name)
VALUES ('101', 'Administracja publiczna');

INSERT INTO ref.Rozdzial (RozdzialCode, DzialId, Name)
VALUES ('1010', 1, 'Wydatki administracyjne ogólne');

INSERT INTO ref.Paragraf (ParagrafCode, Name)
VALUES ('100', 'Wynagrodzenia osobowe');

INSERT INTO ref.SourceOfFunding (SourceCode, Name)
VALUES ('1', 'Środki własne');

INSERT INTO ref.ExpenseGroup (Name)
VALUES ('Wynagrodzenia');

INSERT INTO ref.BudgetTask (FullCode, FunctionNo, TaskNo)
VALUES ('06.03.01.04', '06', '03');

INSERT INTO org.OrganizationalUnit (Code, Name)
VALUES ('DIT', 'Departament Informatyki');

INSERT INTO dim.Dysponent (Name)
VALUES ('Dyrektor Finansowy');

INSERT INTO dbo.BudgetLine
(
  BudgetPartId, DzialId, RozdzialId, ParagrafId, SourceId,
  ExpenseGroupId, BudgetTaskId, OrgUnitId, DysponentId,
  Amount
)
VALUES (1, 1, 1, 1, 1, 1, 1, 1, 1, 10000.00);
