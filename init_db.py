import asyncio
from sqlalchemy import text
from db.database import engine
from db.models.base import Base
# Barcha modellarni import qilamiz (Base.metadata ga registratsiya uchun)
from db.models import *


async def init_db():
    async with engine.begin() as conn:
        print("Creating/updating tables (CREATE IF NOT EXISTS)...")
        # drop_all qilmaymiz — faqat yangi jadvallarni qo'shamiz
        await conn.run_sync(Base.metadata.create_all)
        # UC sotish rejimi olib tashlangan: eski UC mahsulotlari do'kondan yashiriladi
        await conn.execute(text("UPDATE products SET is_active = FALSE WHERE product_type = 'uc' AND is_active = TRUE"))
        # Mahsulot o'chirilganda buyurtma tarixi saqlansin (mavjud bazada FK ni yangilaymiz)
        try:
            async with conn.begin_nested():  # SAVEPOINT — xato bo'lsa qolgan ishlar buzilmaydi
                await conn.execute(text("ALTER TABLE orders DROP CONSTRAINT IF EXISTS orders_product_id_fkey"))
                await conn.execute(text(
                    "ALTER TABLE orders ADD CONSTRAINT orders_product_id_fkey "
                    "FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL"))
        except Exception as e:
            print(f"⚠️ orders FK yangilanmadi: {e}")
        # Buyurtma raqamlari uchun ketma-ketlik (xaridlar uchun majburiy)
        await conn.execute(text("CREATE SEQUENCE IF NOT EXISTS order_number_seq START 1"))
        print("✅ Tables created successfully!")


if __name__ == "__main__":
    asyncio.run(init_db())
