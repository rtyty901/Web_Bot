# 환경 변수에서 API 키 가져오기
import os
from dotenv import load_dotenv
load_dotenv()

# langchain 패키지
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import gradio as gr

# RAG Chain 구현을 위한 패키지
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

# 벡터 저장소 캐싱을 위한 전역 변수
vectorstore_cache = {}


# 웹 페이지를 스크래핑하여 벡터 저장소에 저장
def load_web_to_vector_store(url, chunk_size=1000, chunk_overlap=200, cache_key=None):
    """
    웹 페이지를 스크래핑하여 벡터 저장소에 저장합니다.
    
    Args:
        url: 웹 페이지 URL
        chunk_size: 청크 크기
        chunk_overlap: 청크 오버랩 크기
        cache_key: 캐시 키 (None이면 URL 사용)
    
    Returns:
        FAISS 벡터 저장소 인스턴스
    """
    try:
        # 캐시 키 생성
        if cache_key is None:
            cache_key = f"{url}_{chunk_size}_{chunk_overlap}"
        
        # 캐시 확인
        if cache_key in vectorstore_cache:
            return vectorstore_cache[cache_key]
        
        # URL 유효성 검사
        if not url or not url.strip():
            raise ValueError("URL이 입력되지 않았습니다.")
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url.strip()
        
        # 웹 페이지 로딩
        print(f"웹 페이지 스크래핑 중: {url}")
        loader = WebBaseLoader(url)
        documents = loader.load()
        
        if not documents:
            raise ValueError("웹 페이지에서 내용을 추출할 수 없습니다.")
        
        # 텍스트 분할
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        splits = text_splitter.split_documents(documents)
        
        # FAISS 벡터 저장소 생성 및 문서 임베딩으로 초기화
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)
        
        # 캐시에 저장
        vectorstore_cache[cache_key] = vectorstore
        
        return vectorstore
    except Exception as e:
        raise Exception(f"웹 스크래핑 중 오류 발생: {str(e)}")


# 벡터 저장소에서 문서를 검색하고 답변을 생성
def retrieve_and_generate_answers(vectorstore, message, temperature=0):
    """
    벡터 저장소에서 관련 문서를 검색하고 RAG를 통해 답변을 생성합니다.
    
    Args:
        vectorstore: FAISS 벡터 저장소 인스턴스
        message: 사용자 질문
        temperature: 모델 온도 설정
    
    Returns:
        생성된 답변 문자열
    """
    try:
        if not message or not message.strip():
            return "질문을 입력해주세요."
        
        # RAG 체인 생성
        retriever = vectorstore.as_retriever()

        # Prompt
        template = '''Answer the question based only on the following context from the web page:
<context>
{context}
</context>

Question: {input}

Provide a clear and concise answer based only on the provided context. If the context doesn't contain enough information to answer the question, say so.'''

        prompt = ChatPromptTemplate.from_template(template)

        # ChatModel 인스턴스 생성
        model = ChatOpenAI(model='gpt-4o-mini', 
                           temperature=temperature)

        # LCEL을 사용한 RAG 체인 구성
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        
        rag_chain = (
            {"context": retriever | RunnableLambda(format_docs), "input": RunnablePassthrough()}
            | prompt
            | model
            | StrOutputParser()
        )

        # 검색 결과를 바탕으로 답변 생성
        answer = rag_chain.invoke(message)

        return answer
    except Exception as e:
        return f"답변 생성 중 오류가 발생했습니다: {str(e)}"


# Gradio 인터페이스에서 사용할 함수
def process_web_and_answer(message, history, url, chunk_size, chunk_overlap, temperature):
    """
    웹 페이지를 스크래핑하고 질문에 답변하는 메인 함수입니다.
    
    Args:
        message: 사용자 질문
        history: 대화 기록
        url: 웹 페이지 URL
        chunk_size: 청크 크기
        chunk_overlap: 청크 오버랩
        temperature: 모델 온도
    
    Returns:
        생성된 답변
    """
    try:
        # URL이 없으면 오류 메시지 반환
        if url is None or not url.strip():
            return "웹 페이지 URL을 먼저 입력해주세요."
        
        # 입력 값 검증
        chunk_size = int(chunk_size) if chunk_size else 1000
        chunk_overlap = int(chunk_overlap) if chunk_overlap else 200
        temperature = float(temperature) if temperature else 0.0
        
        # 유효성 검사
        if chunk_size <= 0:
            return "Chunk Size는 0보다 커야 합니다."
        if chunk_overlap < 0:
            return "Chunk Overlap은 0 이상이어야 합니다."
        if chunk_overlap >= chunk_size:
            return "Chunk Overlap은 Chunk Size보다 작아야 합니다."
        if temperature < 0 or temperature > 2:
            return "Temperature는 0과 2 사이의 값이어야 합니다."
        
        # URL 정규화
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # 캐시 키 생성 (URL + 설정값)
        cache_key = f"{url}_{chunk_size}_{chunk_overlap}"
        
        # 벡터 저장소 로드 (캐시 사용)
        vectorstore = load_web_to_vector_store(
            url, 
            chunk_size, 
            chunk_overlap, 
            cache_key=cache_key
        )

        # 답변 생성
        answer = retrieve_and_generate_answers(vectorstore, message, temperature)

        return answer
    except ValueError as e:
        return f"입력 값 오류: {str(e)}"
    except Exception as e:
        return f"처리 중 오류가 발생했습니다: {str(e)}"


# Gradio 인터페이스 생성
demo = gr.ChatInterface(
    fn=process_web_and_answer,
    title="Web Scraping RAG 챗봇",
    description="""웹 페이지 URL을 입력하고 내용에 대해 질문하세요!
    
**사용 방법:**
1. 아래 "Additional Inputs" 섹션을 클릭하여 펼치기
2. "웹 페이지 URL" 입력란에 URL 입력 (예: https://example.com)
3. 질문을 입력하고 전송하기

**지원 형식:** 
- 모든 HTTP/HTTPS 웹 페이지 URL
- http:// 또는 https:// 없이 입력해도 자동으로 추가됩니다""",
    additional_inputs=[
        gr.Textbox(label="🌐 웹 페이지 URL (필수)", 
                   placeholder="https://example.com 또는 example.com",
                   value=""),
        gr.Number(label="Chunk Size", value=1000, minimum=100, maximum=5000, step=100),
        gr.Number(label="Chunk Overlap", value=200, minimum=0, maximum=1000, step=50),
        gr.Slider(label="Temperature", minimum=0, maximum=2, step=0.1, value=0.0),
    ],
    examples=[
        ["이 웹페이지의 주요 내용은 무엇인가요?", "https://www.python.org", 1000, 200, 0.0],
        ["핵심 내용을 요약해주세요.", "https://www.python.org", 1000, 200, 0.0],
    ],
)

# 애플리케이션 실행
if __name__ == "__main__":
    # API 키 확인
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ 경고: OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")
        print("   .env 파일에 OPENAI_API_KEY를 설정해주세요.")
    
    demo.launch(share=False)
