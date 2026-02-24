from src.main import app
from src.database import db
from src.models.invoice_unified import Invoice

app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI="sqlite:///:memory:")

with app.app_context():
    db.drop_all()
    db.create_all()

    inv = Invoice(
        invoice_number="X",
        invoice_type="sales",
        status="draft",
        total_amount=1.0,
    )
    db.session.add(inv)
    db.session.commit()

    print("inserted id", inv.id)

    try:
        rows = Invoice.query.all()
        print("queried invoice_type", rows[0].invoice_type, type(rows[0].invoice_type))
        print("queried status", rows[0].status, type(rows[0].status))
    except Exception as e:
        print("query failed:", type(e), e)
