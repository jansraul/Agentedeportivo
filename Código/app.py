from langchain_openai import ChatOpenAI
import os
from flask import Flask, jsonify, request
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage
from langchain_openai import OpenAIEmbeddings
from langchain_elasticsearch import ElasticsearchStore
from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.prebuilt import create_react_agent


## datos de trazabilidad
os.environ["LANGSMITH_ENDPOINT"]="https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.environ.get("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "agentsport"
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")


app = Flask(__name__)

@app.route('/agent', methods=['GET'])
def main():
    #Capturamos variables enviadas
    id_agente = request.args.get('idagente')
    msg = request.args.get('msg')
    #datos de configuracion
    DB_URI = os.environ["DB_URI"]
    connection_kwargs = {
        "autocommit": True,
        "prepare_threshold": 0,
    }
    db_query = ElasticsearchStore(
        es_url="http://35.1xx.61.211:9200",
        es_user="elastic",
        es_password="claveelaticsearch",
        index_name="elasticsportj-data",
        embedding=OpenAIEmbeddings())

    # Herramienta RAG
    retriever = db_query.as_retriever()
    tool_rag = retriever.as_tool(
        name="busqueda_productos",
        description="Consulta en la informacion de implementos de artes marciales mixtas, running, levantamiento de pesas, suplementos deportivos, y medicina deportiva",
    )
    # Inicializamos la memoria
    with ConnectionPool(
            # Example configuration
            conninfo=DB_URI,
            max_size=20,
            kwargs=connection_kwargs,
    ) as pool:
        checkpointer = PostgresSaver(pool)

        # Inicializamos el modelo
        model = ChatOpenAI(model="gpt-4.1-2025-04-14")

        # Agrupamos las herramientas
        tolkit = [tool_rag]

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system",
        """
        Eres un asesor experto en ventas deportivas, amable y entusiasta. Tu objetivo es guiar a los clientes en la compra de implementos para artes marciales mixtas, running, pesas, suplementos y medicina deportiva.

        Siempre utiliza las herramientas disponibles para obtener la información de productos (nombre, descripción, precio, stock). No inventes si no tienes información; en su lugar, guía con recomendaciones generales.

        Tu estilo debe ser conversacional, breve, directo y con un tono cálido, como un amigo que sabe mucho de deportes. Guía al cliente paso a paso:

        1. Saludo inicial:
           - Da una bienvenida cercana (ej. “¡Hola campeón! ¿Qué estás buscando hoy para tu rutina?”).
           - Pregunta si el cliente ya tiene en mente lo que necesita o si desea sugerencias.
           - Si no sabe, ofrece 2-3 opciones populares (por categoría), priorizando productos con más stock.

        2. Consulta de productos:
           - Filtra productos según lo que necesita el cliente.
           - Muestra nombre, breve descripción, precio y disponibilidad.
           - Si hay stock limitado, avisa. Si hay buen stock, anímalo con frases como “¡Aprovecha que está disponible!”.

        3. Envío o tienda:
           - Pregunta si quiere recoger en tienda o envío a domicilio.
           - Informa: Envío cuesta S/20 si la compra es menor a S/500. Si supera S/500, el envío es gratis.
           - Si está cerca del límite, sugiere productos complementarios útiles para llegar al envío gratis.

        4. Confirmación:
           - Resume el pedido actual y pregunta si quiere añadir algo más.

        5. Método de pago:
           - Si elige tienda, pregunta si pagará en efectivo o por transferencia.
           - Pide su nombre y apellido para generar un código de pedido (formato: AAAAMMDD_HHMMSS_NombreApellido).
           - Si elige domicilio, pide dirección completa y confirma pago por transferencia.

        6. Cierre:
           - Si es transferencia, da el número de cuenta: 12730317292820 en BankaNet y solicita confirmación.
           - Si paga en tienda, entrega el código de pedido y agradece su compra.

        7. Estilo:
           - Sé claro, breve y útil.
           - Usa expresiones como “¡Vamos con todo!”, “¡Listo campeón!”, “Perfecto, crack”.

        IMPORTANTE:
        - Siempre consulta a Elasticsearch antes de dar detalles de productos.
        - No hables como robot. Sé fresco, humano, motivador.
        """),
                ("human", "{messages}"),
            ]
        )
        # inicializamos el agente
        agent_executor = create_react_agent(model, tolkit, checkpointer=checkpointer, prompt=prompt)
        # ejecutamos el agente
        config = {"configurable": {"thread_id": id_agente}}
        response = agent_executor.invoke({"messages": [HumanMessage(content=msg)]}, config=config)
        return response['messages'][-1].content


if __name__ == '__main__':
    # La aplicación escucha en el puerto 8080, requerido por Cloud Run
    app.run(host='0.0.0.0', port=8080)
