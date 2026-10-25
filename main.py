from fastapi import FastAPI
from pydantic import BaseModel
from agents import agent, invoice_eligibility_agent, interest_calculation_agent, notice_drafter_agent

app = FastAPI()

class InvoiceData(BaseModel):
    invoice_date: str
    amount: float
    agreed_terms: int
    supplier_name: str
    buyer_name: str
    is_udyam: bool
    business_type: str
    raw_invoice: str | None = None
    
class InvoiceResponse(BaseModel):
    due_date: str
    interest_owed: float
    is_overdue: bool
    eligible: bool
    draft_message: str | None = None
    
@app.post("/invoice_data", response_model=InvoiceResponse)
async def invoice_data(data: InvoiceData) -> InvoiceResponse:
    eligibility_result = invoice_eligibility_agent({"is_udyam": data.is_udyam, "business_type": data.business_type})
    eligiblity = eligibility_result["eligible"]
    dues = interest_calculation_agent({"invoice_date": data.invoice_date, "amount": data.amount, "agreed_terms": data.agreed_terms})
    draft_message = None
    if eligiblity and dues["is_overdue"]:
        raw_invoice = data.raw_invoice or (
            f"Supplier: {data.supplier_name}\n"
            f"Buyer: {data.buyer_name}\n"
            f"Amount: {data.amount}\n"
            f"Invoice date: {data.invoice_date}\n"
            f"Agreed payment terms: {data.agreed_terms} days"
        )
        notice = notice_drafter_agent({
            "supplier_name": data.supplier_name,
            "buyer_name": data.buyer_name,
            "amount": data.amount,
            "due_date": dues["due_date"],
            "interest_owed": dues["interest_owed"],
            "stage": "initial",
            "raw_invoice": raw_invoice,
        })
        draft_message = notice["draft_message"]
    return InvoiceResponse(due_date=dues["due_date"], interest_owed=dues["interest_owed"], is_overdue=dues["is_overdue"], eligible=eligiblity, draft_message=draft_message)