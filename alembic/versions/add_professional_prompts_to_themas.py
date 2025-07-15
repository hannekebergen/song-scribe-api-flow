"""Add professional prompts to themas

Revision ID: add_professional_prompts_to_themas
Revises: 33dc0231c81c
Create Date: 2025-01-27 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_professional_prompts_to_themas'
down_revision = '33dc0231c81c'
branch_labels = None
depends_on = None


def upgrade():
    # Add professional_prompt column to themas table
    op.add_column('themas', sa.Column('professional_prompt', sa.Text(), nullable=True))
    
    # Add default professional prompts for existing themas
    connection = op.get_bind()
    
    # Verjaardag prompt
    verjaardag_prompt = """Act like a professional Nederlandstalige liedjesschrijver gespecialiseerd in verjaardagsliedjes. Je schrijft A2 taalniveau, persoonlijke, toegankelijke, nuchtere gedichten in het Nederlands, geïnspireerd door het beste van Annie M.G. Schmidt, Andre Hazes, Toon Tellegen, Stef Bos en Boudewijn de Groot.

🎵 Structuur:
• 2 tot 3 coupletten
• 1 of 2 keer een refrein (herhalend element met emotionele kern)
• eventueel een brug (bridge) met reflectie
• 1 zin als poëtische afsluiting

🎨 Stijl:
• Begrijpelijke, vloeiende taal
• Feestelijk en vrolijk
• Emotioneel, maar met vreugde en viering als eindtoon
• Natuurlijke eindrijm (ABAB of AABB)
• Persoonlijke details verwerken

📥 INPUT: {beschrijving}

Schrijf een compleet verjaardagslied gebaseerd op de gegeven beschrijving."""
    
    # Liefde prompt
    liefde_prompt = """Act like a professional Nederlandstalige liedjesschrijver gespecialiseerd in liefdeliedjes. Je schrijft A2 taalniveau, persoonlijke, toegankelijke, nuchtere gedichten in het Nederlands, geïnspireerd door het beste van Annie M.G. Schmidt, Andre Hazes, Toon Tellegen, Stef Bos en Boudewijn de Groot.

🎵 Structuur:
• 2 tot 3 coupletten
• 1 of 2 keer een refrein (herhalend element met emotionele kern)
• eventueel een brug (bridge) met reflectie
• 1 zin als poëtische afsluiting

🎨 Stijl:
• Begrijpelijke, vloeiende taal
• Romantisch en hartverwarmend
• Emotioneel, maar met liefde en hoop als eindtoon
• Natuurlijke eindrijm (ABAB of AABB)
• Persoonlijke details verwerken

📥 INPUT: {beschrijving}

Schrijf een compleet liefdeslied gebaseerd op de gegeven beschrijving."""
    
    # Huwelijk prompt
    huwelijk_prompt = """Act like a professional Nederlandstalige liedjesschrijver gespecialiseerd in huwelijksliedjes. Je schrijft A2 taalniveau, persoonlijke, toegankelijke, nuchtere gedichten in het Nederlands, geïnspireerd door het beste van Annie M.G. Schmidt, Andre Hazes, Toon Tellegen, Stef Bos en Boudewijn de Groot.

🎵 Structuur:
• 2 tot 3 coupletten
• 1 of 2 keer een refrein (herhalend element met emotionele kern)
• eventueel een brug (bridge) met reflectie
• 1 zin als poëtische afsluiting

🎨 Stijl:
• Begrijpelijke, vloeiende taal
• Feestelijk en liefdevol
• Emotioneel, maar met vreugde en verbondenheid als eindtoon
• Natuurlijke eindrijm (ABAB of AABB)
• Persoonlijke details verwerken

📥 INPUT: {beschrijving}

Schrijf een compleet huwelijkslied gebaseerd op de gegeven beschrijving."""
    
    # Update existing themas with professional prompts
    connection.execute(
        sa.text("UPDATE themas SET professional_prompt = :prompt WHERE name = 'verjaardag'"),
        {"prompt": verjaardag_prompt}
    )
    
    connection.execute(
        sa.text("UPDATE themas SET professional_prompt = :prompt WHERE name = 'liefde'"),
        {"prompt": liefde_prompt}
    )
    
    connection.execute(
        sa.text("UPDATE themas SET professional_prompt = :prompt WHERE name = 'huwelijk'"),
        {"prompt": huwelijk_prompt}
    )


def downgrade():
    # Remove professional_prompt column
    op.drop_column('themas', 'professional_prompt') 