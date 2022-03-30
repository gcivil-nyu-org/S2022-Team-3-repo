from django.contrib.postgres.search import SearchVector
from django.db import migrations


def compute_search_vector(apps, schema_editor):
    Post = apps.get_model("reuse", "Post")
    Post.objects.update(search_vector=SearchVector("title", "description", "category"))


class Migration(migrations.Migration):

    dependencies = [
        ("reuse", "0003_rename_search_token_post_search_vector"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE TRIGGER search_vector_trigger
            BEFORE INSERT OR UPDATE OF title, description, category, search_vector
            ON reuse_post
            FOR EACH ROW EXECUTE PROCEDURE
            tsvector_update_trigger(
                search_vector, 'pg_catalog.english', title, description, category
            );
            UPDATE reuse_post SET search_vector = NULL;
            """,
            reverse_sql="""
            DROP TRIGGER IF EXISTS search_vector_trigger
            ON reuse_post;
            """,
        ),
        migrations.RunPython(
            compute_search_vector, reverse_code=migrations.RunPython.noop
        ),
    ]
