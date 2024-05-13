from langchain_core.runnables import RunnableLambda


def suma(a):
    return a + 7


def multiplica(c):
    return c * 2


def reverso(s: str) -> str:
    return s[::-1]


suma = RunnableLambda(suma)
multiplica = RunnableLambda(multiplica)
reverso = RunnableLambda(reverso)

chain = suma | multiplica | str | reverso

result = chain.invoke(234)
print(result)
