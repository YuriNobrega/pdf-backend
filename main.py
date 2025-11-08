from fastapi import FastAPI, Form
from fastapi.responses import StreamingResponse
from pathlib import Path
import io
from PyPDFForm import PdfWrapper
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PDF_MODELS={
    "req-int-venda": Path("PDFs/ReqIntVenda.pdf"),
    "segunda_via_crv": Path("PDFs/crv_segunda_via.pdf"),
    "cancelamento_venda": Path("PDFs/cancelamento_venda.pdf"),
    "comunicado_venda" : Path("PDFs/comunicado_venda.pdf"),
    "alter_carac": Path("PDFs/alter_carac.pdf"),
    "cancelamento_intencao_venda": Path("PDFs/cancelamento_intencao_venda.pdf"),
    "declaracao_endereco": Path("PDFs/declaracao_endereco.pdf"),
    "declaracao_motor": Path("PDFs/declaracao_motor.pdf"),
}




@app.post("/api/pdf/req-int-venda")
async def fill_pdf(
    VendaName: str = Form(""),
    VendaDoc: str = Form(""),
    VendaAddress: str = Form(""),
    VendaCity: str = Form(""),
    VendaEmail: str = Form(""),
    CompraName: str = Form(""),
    CompraDoc: str = Form(""),
    CompraAddress: str = Form(""),
    CompraCity: str = Form(""),
    CompraEmail: str = Form(""),
    Placa: str = Form(""),
    Renavam: str = Form(""),
    Value: str = Form(""),
    Day: str = Form(""),
    Month: str = Form(""),
    Year: str = Form(""),
    DocumentCity: str = Form(""),
    MonthName: str = Form(""),
    SignatureDay: str = Form(""),
    SignatureYear: str = Form("")
):
    pdf_template = PDF_MODELS["req-int-venda"]
    if not pdf_template.exists():
        return {"error": f"Modelo PDF não encontrado em {pdf_template}"}

    # Dicionário de dados
    form_data = {
        "VendaName": VendaName,
        "VendaDoc": VendaDoc,
        "VendaAddress": VendaAddress,
        "VendaCity": VendaCity,
        "VendaEmail": VendaEmail,
        "CompraName": CompraName,
        "CompraDoc": CompraDoc,
        "CompraAddress": CompraAddress,
        "CompraCity": CompraCity,
        "CompraEmail": CompraEmail,
        "Placa": Placa,
        "Renavam": Renavam,
        "Value": Value,
        "Day": Day,
        "Month": Month,
        "Year": Year,
        "DocumentCity": DocumentCity,
        "MonthName": MonthName,
        "SignatureDay": SignatureDay,
        "SignatureYear": SignatureYear
    }

    # Usando PyPDFForm para preencher
    pdf = PdfWrapper(str(pdf_template), adobe_mode=True)
    filled_pdf_bytes = pdf.fill(form_data, flatten=True).read()

    # Retornar para download
    output = io.BytesIO(filled_pdf_bytes)
    return StreamingResponse(
        output,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=Requerimento_Preenchido.pdf"}
    )

@app.post("/api/pdf/crv-segunda-via")
async def fill_crv_segunda_via(
    Nome: str = Form(""),
    CPF_CNPJ: str = Form(""),
    RG: str = Form(""),
    PerdaExtravio: bool = Form(False),
    RasuraErro: bool = Form(False),
    Pericia: bool = Form(False),
    Outros: bool = Form(False),
    Placa: str = Form(""),
    Renavam: str = Form(""),
    Cidade: str = Form(""),
    Dia: str = Form(""),
    Mes: str = Form(""),
    Ano: str = Form(""),
):
    pdf_template = PDF_MODELS["segunda_via_crv"]
    if not pdf_template.exists():
        return {"error": f"Modelo PDF não encontrado em {pdf_template}"}

    # Dicionário de preenchimento — as chaves DEVEM bater com os "names" no PDF
    data = {
        "Nome": Nome,
        "CPF_CNPJ": CPF_CNPJ,
        "RG": RG,
        "PerdaExtravio": PerdaExtravio,
        "RasuraErro": RasuraErro,
        "Pericia": Pericia,
        "Outros": Outros,
        "Placa": Placa,
        "Renavam": Renavam,
        "Cidade": Cidade,
        "Dia": Dia,
        "Mes": Mes,
        "Ano": Ano,
    }

    # Preenche e achata (flatten) para evitar discrepâncias de renderização
    pdf = PdfWrapper(str(pdf_template), adobe_mode=True)
    filled = pdf.fill(data, flatten=True).read()

    return StreamingResponse(
        io.BytesIO(filled),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=CRV_Segunda_Via.pdf"},
    )

@app.post("/api/pdf/cancelamento-venda")
async def cancelamento_venda(
    Nome: str = Form(""),
    CPF_CNPJ: str = Form(""),
    Telefone: str = Form(""),
    Placa: str = Form(""),
    Renavam: str = Form(""),
    Cidade: str = Form(""),
    Dia: str = Form(""),
    Mes: str = Form(""),
    Ano: str = Form("")
):
    pdf_template = PDF_MODELS["cancelamento_venda"]
    if not pdf_template.exists():
        return {"error": f"Modelo PDF não encontrado em {pdf_template}"}

    # Dicionário de dados do PDF
    form_data = {
        "Nome": Nome,
        "CPF_CNPJ": CPF_CNPJ,
        "Telefone": Telefone,
        "Placa": Placa,
        "Renavam": Renavam,
        "Cidade": Cidade,
        "Dia": Dia,
        "Mes": Mes,
        "Ano": Ano,
    }

    pdf = PdfWrapper(str(pdf_template), adobe_mode=True)
    filled_pdf_bytes = pdf.fill(form_data, flatten=True).read()

    output = io.BytesIO(filled_pdf_bytes)
    return StreamingResponse(
        output,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=Cancelamento_Comunicado_Venda.pdf"}
    )



@app.post("/api/pdf/comunicado-venda")
async def comunicado_venda(
    Nome_Vendedor: str = Form(""),
    CPF_CNPJ_Vendedor: str = Form(""),
    Telefone_Vendedor: str = Form(""),

    Nome_Comprador: str = Form(""),
    CPF_CNPJ_Comprador: str = Form(""),

    Placa: str = Form(""),
    Renavam: str = Form(""),

    Dia_Venda: str = Form(""),
    Mes_Venda: str = Form(""),
    Ano_Venda: str = Form(""),

    Cidade: str = Form(""),
    Dia_Doc: str = Form(""),
    Mes_Doc: str = Form(""),
    Ano_Doc: str = Form("")
):
    pdf_template = PDF_MODELS.get("comunicado_venda")
    if not pdf_template or not pdf_template.exists():
        return {"error": f"Modelo PDF não encontrado em {pdf_template}"}

    # Dicionário de dados do PDF
    form_data = {
        "Nome_Vendedor": Nome_Vendedor,
        "CPF_CNPJ_Vendedor": CPF_CNPJ_Vendedor,
        "Telefone_Vendedor": Telefone_Vendedor,

        "Nome_Comprador": Nome_Comprador,
        "CPF_CNPJ_Comprador": CPF_CNPJ_Comprador,

        "Placa": Placa,
        "Renavam": Renavam,

        "Dia_Venda": Dia_Venda,
        "Mes_Venda": Mes_Venda,
        "Ano_Venda": Ano_Venda,

        "Cidade": Cidade,
        "Dia_Doc": Dia_Doc,
        "Mes_Doc": Mes_Doc,
        "Ano_Doc": Ano_Doc,
    }

    pdf = PdfWrapper(str(pdf_template), adobe_mode=True)
    filled_pdf_bytes = pdf.fill(form_data, flatten=True).read()

    output = io.BytesIO(filled_pdf_bytes)
    return StreamingResponse(
        output,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=Comunicado_Venda.pdf"}
    )

@app.post("/api/pdf/alter-carac")
async def alter_carac(
    Nome: str = Form(""),
    CPF_CNPJ: str = Form(""),
    Alteracao: str = Form(""),

    Placa: str = Form(""),
    Renavam: str = Form(""),

    Cidade: str = Form(""),
    Dia: str = Form(""),
    Mes: str = Form(""),
    Ano: str = Form("")
):
    pdf_template = PDF_MODELS.get("alter_carac")
    if not pdf_template or not pdf_template.exists():
        return {"error": f"Modelo PDF não encontrado em {pdf_template}"}

    form_data = {
        "Nome": Nome,
        "CPF_CNPJ": CPF_CNPJ,
        "Alteracao": Alteracao,

        "Placa": Placa,
        "Renavam": Renavam,

        "Cidade": Cidade,
        "Dia": Dia,
        "Mes": Mes,
        "Ano": Ano,
    }

    pdf = PdfWrapper(str(pdf_template), adobe_mode=True)
    filled_pdf_bytes = pdf.fill(form_data, flatten=True).read()

    output = io.BytesIO(filled_pdf_bytes)
    return StreamingResponse(
        output,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=Alteracao_Caracteristica.pdf"}
    )


@app.post("/api/pdf/cancelamento-intencao-venda")
async def cancelamento_intencao_venda(
    NomeVendedor: str = Form(""),
    CPF_CNPJVendedor: str = Form(""),
    EnderecoVendedor: str = Form(""),
    EmailVendedor: str = Form(""),
    MunicipioVendedor: str = Form(""),

    NomeComprador: str = Form(""),
    CPF_CNPJComprador: str = Form(""),
    EnderecoComprador: str = Form(""),
    MunicipioComprador: str = Form(""),
    EmailComprador: str = Form(""),

    Placa: str = Form(""),
    Renavam: str = Form(""),

    Cidade: str = Form(""),
    Dia: str = Form(""),
    Mes: str = Form(""),
    Ano: str = Form("")
):
    pdf_template = PDF_MODELS.get("cancelamento_intencao_venda")
    if not pdf_template or not pdf_template.exists():
        return {"error": f"Modelo PDF não encontrado em {pdf_template}"}

    form_data = {
        "NomeVendedor": NomeVendedor,
        "CPF_CNPJVendedor": CPF_CNPJVendedor,
        "EnderecoVendedor": EnderecoVendedor,
        "EmailVendedor": EmailVendedor,
        "MunicipioVendedor": MunicipioVendedor,

        "NomeComprador": NomeComprador,
        "CPF_CNPJComprador": CPF_CNPJComprador,
        "EnderecoComprador": EnderecoComprador,
        "MunicipioComprador": MunicipioComprador,
        "EmailComprador": EmailComprador,

        "Placa": Placa,
        "Renavam": Renavam,

        "Cidade": Cidade,
        "Dia": Dia,
        "Mes": Mes,
        "Ano": Ano,
    }

    pdf = PdfWrapper(str(pdf_template),adobe_mode=True)
    filled_pdf_bytes = pdf.fill(form_data,flatten=True).read()

    output = io.BytesIO(filled_pdf_bytes)
    return StreamingResponse(
        output,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=Cancelamento_Intencao_Venda.pdf"}
    )

@app.post("/api/pdf/declaracao-motor")
async def declaracao_motor(
    Nome: str = Form(""),
    CPF_CNPJ: str = Form(""),
    RG: str = Form(""),

    Rua: str = Form(""),
    Numero: str = Form(""),
    Bairro: str = Form(""),
    Municipio: str = Form(""),
    Estado: str = Form(""),
    
    
    Motor: str = Form(""),


    Placa: str = Form(""),
    Chassi: str = Form(""),
    Marca: str = Form(""),


    Cidade: str = Form(""),
    Dia: str = Form(""),
    Mes: str = Form(""),
    Ano: str = Form("")
):
    pdf_template = PDF_MODELS.get("declaracao_motor")
    if not pdf_template or not pdf_template.exists():
        return {"error": f"Modelo PDF não encontrado em {pdf_template}"}

    # Dicionário de dados do PDF
    form_data = {
        "Nome": Nome,
        "CPF_CNPJ": CPF_CNPJ,
        "RG": RG,
        
        
        "Rua": Rua,
        "Numero": Numero,
        "Bairro": Bairro,
        "Estado": Estado,
        "Municipio": Municipio,
        
        "Motor": Motor,


        "Placa": Placa,
        "Chassi": Chassi,
        "Marca": Marca,


        "Cidade": Cidade,
        "Dia": Dia,
        "Mes": Mes,
        "Ano": Ano,
    }

    pdf = PdfWrapper(str(pdf_template), adobe_mode=True)
    filled_pdf_bytes = pdf.fill(form_data,flatten=True).read()

    output = io.BytesIO(filled_pdf_bytes)
    return StreamingResponse(
        output,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=declaracao_motor.pdf"}
    )

@app.post("/api/pdf/declaracao-endereco")
async def declaracao_endereco(
    Nome: str = Form(""),
    RG: str = Form(""),
    CPF: str = Form(""),  # Recebe CPF completo (com ou sem pontuação)

    Endereco1: str = Form(""),
    Endereco2: str = Form(""),
    Numero: str = Form(""),
    Bairro: str = Form(""),
    Cidade: str = Form(""),
    CEP: str = Form(""),
    DDD: str = Form(""),
    Telefone: str = Form(""),

    CidadeDoc: str = Form(""),
    Dia: str = Form(""),
    Mes: str = Form(""),
    Ano: str = Form("")
):
    pdf_template = PDF_MODELS.get("declaracao_endereco")
    if not pdf_template or not pdf_template.exists():
        return {"error": f"Modelo PDF não encontrado em {pdf_template}"}

    # -------------------------
    # TRATAMENTO DO CPF
    # -------------------------
    # Remove pontos e traços, mantendo apenas números
    cpf_numbers = "".join(filter(str.isdigit, CPF))

    if len(cpf_numbers) != 11:
        return {"error": "CPF inválido. Envie no formato XXX.XXX.XXX-XX ou apenas os 11 dígitos."}

    CPF1 = cpf_numbers[0:3]
    CPF2 = cpf_numbers[3:6]
    CPF3 = cpf_numbers[6:9]
    CPF4 = cpf_numbers[9:11]

    # -------------------------
    # FORM DATA
    # -------------------------
    form_data = {
        "Nome": Nome,
        "RG": RG,

        # CPF quebrado
        "CPF1": CPF1,
        "CPF2": CPF2,
        "CPF3": CPF3,
        "CPF4": CPF4,

        # Endereço
        "Endereco1": Endereco1,
        "Endereco2": Endereco2,
        "Numero": Numero,
        "Bairro": Bairro,
        "Cidade": Cidade,
        "CEP": CEP,
        "DDD": DDD,
        "Telefone": Telefone,

        # Local e data
        "CidadeDoc": CidadeDoc,
        "Dia": Dia,
        "Mes": Mes,
        "Ano": Ano,
    }

    pdf = PdfWrapper(str(pdf_template),adobe_mode=True)
    filled_pdf_bytes = pdf.fill(form_data,flatten=True).read()

    output = io.BytesIO(filled_pdf_bytes)
    return StreamingResponse(
        output,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=Declaracao_Endereco.pdf"}
    )

@app.get("/api/pdf/test")
def test():
    return {"message": "PDF Controller is working!"}
