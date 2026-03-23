import pytest_asyncio
from app.models import Link
from sqlalchemy import delete




@pytest_asyncio.fixture(scope='function')
async def mock_links(db_session):
    """Фикстура для создания ссылок."""
    await db_session.execute(delete(Link))
    await db_session.commit()

    links = [
        Link(original_link='https://fastapi.tiangolo.com', short_link='SD4r4G72'),
        Link(original_link='https://stackoverflow.com', short_link='4B6ZRpPO'),
    ]
    db_session.add_all(links)
    await db_session.commit()
    
    for link in links:
        await db_session.refresh(link)
    
    yield links
    
    await db_session.execute(delete(Link))
    await db_session.commit()