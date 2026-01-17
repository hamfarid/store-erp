================================================================================
MODULE 44: DATABASE TESTING
================================================================================
Version: Latest
Last Updated: 2025-11-07
Purpose: Database integrity, relationships, queries, performance
================================================================================

## OVERVIEW

Database testing ensures data integrity, validates relationships, and verifies
query performance. This module covers database testing strategies and best practices.

================================================================================
## WHY DATABASE TESTING?
================================================================================

**Benefits:**
✓ Ensures data integrity
✓ Validates relationships
✓ Catches schema issues
✓ Tests constraints
✓ Verifies indexes
✓ Tests migrations
✓ Validates queries
✓ Tests performance

**When to Test:**
- After schema changes
- After migrations
- Before deployment
- During development
- After data imports
- Performance issues

================================================================================
## TESTING TYPES
================================================================================

### 1. Schema Testing
Verify database structure is correct

### 2. Relationship Testing
Validate foreign keys and cascades

### 3. Constraint Testing
Test unique, not null, check constraints

### 4. Query Testing
Verify queries return correct data

### 5. Performance Testing
Test query speed and optimization

### 6. Migration Testing
Validate migrations work correctly

================================================================================
## SCHEMA TESTING
================================================================================

### PostgreSQL
```python
# tests/test_schema.py
import pytest
from django.db import connection

def test_users_table_exists():
    """Test users table exists"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public'
                AND table_name = 'users'
            );
        """)
        exists = cursor.fetchone()[0]
        assert exists, "users table does not exist"

def test_users_table_columns():
    """Test users table has correct columns"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'users'
            ORDER BY ordinal_position;
        """)
        columns = cursor.fetchall()
        
        expected_columns = {
            'id': ('integer', 'NO'),
            'email': ('character varying', 'NO'),
            'name': ('character varying', 'NO'),
            'created_at': ('timestamp with time zone', 'NO'),
            'updated_at': ('timestamp with time zone', 'NO'),
        }
        
        for col_name, data_type, is_nullable in columns:
            assert col_name in expected_columns
            assert expected_columns[col_name] == (data_type, is_nullable)

def test_indexes_exist():
    """Test required indexes exist"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT indexname
            FROM pg_indexes
            WHERE tablename = 'users';
        """)
        indexes = [row[0] for row in cursor.fetchall()]
        
        assert 'users_pkey' in indexes  # Primary key
        assert 'users_email_key' in indexes  # Unique email
        assert 'users_created_at_idx' in indexes  # Created at index
```

### MySQL
```python
def test_users_table_exists_mysql():
    """Test users table exists (MySQL)"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = DATABASE()
            AND table_name = 'users';
        """)
        count = cursor.fetchone()[0]
        assert count == 1, "users table does not exist"

def test_users_table_engine():
    """Test users table uses InnoDB"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT engine
            FROM information_schema.tables
            WHERE table_schema = DATABASE()
            AND table_name = 'users';
        """)
        engine = cursor.fetchone()[0]
        assert engine == 'InnoDB', f"Expected InnoDB, got {engine}"
```

================================================================================
## RELATIONSHIP TESTING
================================================================================

### Foreign Keys
```python
# tests/test_relationships.py
import pytest
from django.db import IntegrityError
from myapp.models import User, Post, Comment

def test_post_user_relationship():
    """Test post belongs to user"""
    user = User.objects.create(email='user@example.com', name='User')
    post = Post.objects.create(user=user, title='Test Post')
    
    assert post.user == user
    assert user.posts.count() == 1
    assert user.posts.first() == post

def test_cascade_delete():
    """Test cascade delete works"""
    user = User.objects.create(email='user@example.com', name='User')
    post = Post.objects.create(user=user, title='Test Post')
    comment = Comment.objects.create(post=post, text='Test Comment')
    
    # Delete user should delete post and comment
    user.delete()
    
    assert Post.objects.filter(id=post.id).count() == 0
    assert Comment.objects.filter(id=comment.id).count() == 0

def test_foreign_key_constraint():
    """Test foreign key constraint is enforced"""
    with pytest.raises(IntegrityError):
        # Try to create post with non-existent user_id
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO posts (user_id, title)
                VALUES (99999, 'Test Post');
            """)

def test_many_to_many_relationship():
    """Test many-to-many relationship"""
    user1 = User.objects.create(email='user1@example.com', name='User 1')
    user2 = User.objects.create(email='user2@example.com', name='User 2')
    post = Post.objects.create(user=user1, title='Test Post')
    
    # Add likes
    post.likes.add(user1, user2)
    
    assert post.likes.count() == 2
    assert user1 in post.likes.all()
    assert user2 in post.likes.all()
    assert post in user1.liked_posts.all()
```

### Relationship Integrity
```python
def test_orphaned_records():
    """Test no orphaned records exist"""
    with connection.cursor() as cursor:
        # Check for posts without users
        cursor.execute("""
            SELECT COUNT(*)
            FROM posts p
            LEFT JOIN users u ON p.user_id = u.id
            WHERE u.id IS NULL;
        """)
        orphaned_posts = cursor.fetchone()[0]
        assert orphaned_posts == 0, f"Found {orphaned_posts} orphaned posts"
        
        # Check for comments without posts
        cursor.execute("""
            SELECT COUNT(*)
            FROM comments c
            LEFT JOIN posts p ON c.post_id = p.id
            WHERE p.id IS NULL;
        """)
        orphaned_comments = cursor.fetchone()[0]
        assert orphaned_comments == 0, f"Found {orphaned_comments} orphaned comments"
```

================================================================================
## CONSTRAINT TESTING
================================================================================

### Unique Constraints
```python
def test_email_unique_constraint():
    """Test email must be unique"""
    User.objects.create(email='user@example.com', name='User 1')
    
    with pytest.raises(IntegrityError):
        User.objects.create(email='user@example.com', name='User 2')

def test_composite_unique_constraint():
    """Test composite unique constraint"""
    user = User.objects.create(email='user@example.com', name='User')
    Tag.objects.create(user=user, name='python')
    
    with pytest.raises(IntegrityError):
        # Same user + tag name should fail
        Tag.objects.create(user=user, name='python')
```

### Not Null Constraints
```python
def test_required_fields():
    """Test required fields cannot be null"""
    with pytest.raises(IntegrityError):
        User.objects.create(email=None, name='User')
    
    with pytest.raises(IntegrityError):
        User.objects.create(email='user@example.com', name=None)
```

### Check Constraints
```python
def test_check_constraint():
    """Test check constraint is enforced"""
    user = User.objects.create(email='user@example.com', name='User')
    
    # Age must be >= 0
    with pytest.raises(IntegrityError):
        user.age = -1
        user.save()
    
    # Age must be <= 150
    with pytest.raises(IntegrityError):
        user.age = 200
        user.save()
```

================================================================================
## QUERY TESTING
================================================================================

### Basic Queries
```python
def test_filter_query():
    """Test filter query returns correct results"""
    user1 = User.objects.create(email='user1@example.com', name='Alice')
    user2 = User.objects.create(email='user2@example.com', name='Bob')
    user3 = User.objects.create(email='user3@example.com', name='Alice')
    
    results = User.objects.filter(name='Alice')
    
    assert results.count() == 2
    assert user1 in results
    assert user3 in results
    assert user2 not in results

def test_complex_query():
    """Test complex query with joins"""
    user = User.objects.create(email='user@example.com', name='User')
    post1 = Post.objects.create(user=user, title='Post 1', published=True)
    post2 = Post.objects.create(user=user, title='Post 2', published=False)
    Comment.objects.create(post=post1, text='Comment 1')
    Comment.objects.create(post=post1, text='Comment 2')
    
    # Get users with published posts that have comments
    results = User.objects.filter(
        posts__published=True,
        posts__comments__isnull=False
    ).distinct()
    
    assert results.count() == 1
    assert user in results

def test_aggregation_query():
    """Test aggregation query"""
    user = User.objects.create(email='user@example.com', name='User')
    Post.objects.create(user=user, title='Post 1', views=100)
    Post.objects.create(user=user, title='Post 2', views=200)
    Post.objects.create(user=user, title='Post 3', views=300)
    
    from django.db.models import Sum, Avg, Count
    
    stats = Post.objects.filter(user=user).aggregate(
        total_views=Sum('views'),
        avg_views=Avg('views'),
        post_count=Count('id')
    )
    
    assert stats['total_views'] == 600
    assert stats['avg_views'] == 200
    assert stats['post_count'] == 3
```

### Raw SQL Queries
```python
def test_raw_sql_query():
    """Test raw SQL query"""
    user = User.objects.create(email='user@example.com', name='User')
    Post.objects.create(user=user, title='Test Post', views=100)
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT u.name, COUNT(p.id) as post_count, SUM(p.views) as total_views
            FROM users u
            LEFT JOIN posts p ON p.user_id = u.id
            WHERE u.id = %s
            GROUP BY u.id, u.name;
        """, [user.id])
        
        result = cursor.fetchone()
        name, post_count, total_views = result
        
        assert name == 'User'
        assert post_count == 1
        assert total_views == 100
```

================================================================================
## PERFORMANCE TESTING
================================================================================

### Query Performance
```python
import time
from django.test.utils import override_settings

@override_settings(DEBUG=True)
def test_query_performance():
    """Test query executes within acceptable time"""
    # Create test data
    for i in range(1000):
        User.objects.create(email=f'user{i}@example.com', name=f'User {i}')
    
    # Measure query time
    start = time.time()
    users = list(User.objects.filter(name__startswith='User'))
    end = time.time()
    
    query_time = end - start
    assert query_time < 0.1, f"Query took {query_time}s, expected < 0.1s"

def test_n_plus_one_problem():
    """Test no N+1 query problem"""
    from django.test.utils import override_settings
    from django.db import connection, reset_queries
    
    # Create test data
    user = User.objects.create(email='user@example.com', name='User')
    for i in range(10):
        Post.objects.create(user=user, title=f'Post {i}')
    
    with override_settings(DEBUG=True):
        reset_queries()
        
        # Bad: N+1 queries
        posts = Post.objects.all()
        for post in posts:
            _ = post.user.name  # Triggers query for each post
        
        bad_query_count = len(connection.queries)
        
        reset_queries()
        
        # Good: Use select_related
        posts = Post.objects.select_related('user').all()
        for post in posts:
            _ = post.user.name  # No additional queries
        
        good_query_count = len(connection.queries)
        
        assert good_query_count < bad_query_count
        assert good_query_count <= 2  # 1 query for posts + users

def test_index_usage():
    """Test query uses index"""
    user = User.objects.create(email='user@example.com', name='User')
    
    with connection.cursor() as cursor:
        # PostgreSQL: Check query plan
        cursor.execute("""
            EXPLAIN (FORMAT JSON)
            SELECT * FROM users WHERE email = %s;
        """, ['user@example.com'])
        
        plan = cursor.fetchone()[0]
        
        # Should use index scan, not sequential scan
        assert 'Index Scan' in str(plan) or 'Bitmap Index Scan' in str(plan)
        assert 'Seq Scan' not in str(plan)
```

### Database Size
```python
def test_database_size():
    """Test database size is within limits"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT pg_size_pretty(pg_database_size(current_database()));
        """)
        size = cursor.fetchone()[0]
        
        # Parse size (e.g., "10 MB")
        size_value = float(size.split()[0])
        size_unit = size.split()[1]
        
        # Convert to MB
        if size_unit == 'GB':
            size_mb = size_value * 1024
        elif size_unit == 'kB':
            size_mb = size_value / 1024
        else:
            size_mb = size_value
        
        # Database should be < 1GB
        assert size_mb < 1024, f"Database size is {size}, expected < 1GB"
```

================================================================================
## MIGRATION TESTING
================================================================================

### Test Migrations
```python
# tests/test_migrations.py
from django.core.management import call_command
from django.db.migrations.executor import MigrationExecutor
from django.db import connection

def test_migrations_apply_cleanly():
    """Test all migrations apply without errors"""
    call_command('migrate', verbosity=0)
    
    executor = MigrationExecutor(connection)
    plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
    
    # All migrations should be applied
    assert len(plan) == 0, "Not all migrations are applied"

def test_migration_reversible():
    """Test migration can be reversed"""
    # Get current migration
    executor = MigrationExecutor(connection)
    current_state = executor.loader.project_state()
    
    # Migrate back
    call_command('migrate', 'myapp', '0001', verbosity=0)
    
    # Migrate forward again
    call_command('migrate', 'myapp', verbosity=0)
    
    # Should be back to current state
    new_state = executor.loader.project_state()
    assert current_state.apps.get_models() == new_state.apps.get_models()

def test_migration_data_integrity():
    """Test migration preserves data"""
    # Create test data
    user = User.objects.create(email='user@example.com', name='User')
    post = Post.objects.create(user=user, title='Test Post')
    
    # Run migration
    call_command('migrate', verbosity=0)
    
    # Check data still exists
    assert User.objects.filter(id=user.id).exists()
    assert Post.objects.filter(id=post.id).exists()
    
    # Check relationships intact
    post_after = Post.objects.get(id=post.id)
    assert post_after.user.id == user.id
```

================================================================================
## TRANSACTION TESTING
================================================================================

### Test Transactions
```python
from django.db import transaction

def test_transaction_rollback():
    """Test transaction rolls back on error"""
    initial_count = User.objects.count()
    
    try:
        with transaction.atomic():
            User.objects.create(email='user1@example.com', name='User 1')
            User.objects.create(email='user2@example.com', name='User 2')
            
            # Force error
            raise Exception("Test error")
    except Exception:
        pass
    
    # No users should be created
    assert User.objects.count() == initial_count

def test_transaction_commit():
    """Test transaction commits on success"""
    initial_count = User.objects.count()
    
    with transaction.atomic():
        User.objects.create(email='user1@example.com', name='User 1')
        User.objects.create(email='user2@example.com', name='User 2')
    
    # Both users should be created
    assert User.objects.count() == initial_count + 2
```

================================================================================
## DATA VALIDATION TESTING
================================================================================

### Test Data Validation
```python
def test_email_validation():
    """Test email validation"""
    from django.core.exceptions import ValidationError
    
    # Valid email
    user = User(email='user@example.com', name='User')
    user.full_clean()  # Should not raise
    
    # Invalid email
    user = User(email='invalid-email', name='User')
    with pytest.raises(ValidationError):
        user.full_clean()

def test_data_sanitization():
    """Test data is sanitized"""
    user = User.objects.create(
        email='  USER@EXAMPLE.COM  ',
        name='  User Name  '
    )
    
    # Email should be lowercase and trimmed
    assert user.email == 'user@example.com'
    
    # Name should be trimmed
    assert user.name == 'User Name'
```

================================================================================
## BACKUP AND RESTORE TESTING
================================================================================

### Test Backup
```bash
# Backup database
pg_dump -U postgres -d mydb > backup.sql

# Restore database
psql -U postgres -d mydb_test < backup.sql
```

```python
def test_backup_restore():
    """Test database can be backed up and restored"""
    import subprocess
    
    # Create test data
    user = User.objects.create(email='user@example.com', name='User')
    
    # Backup
    subprocess.run([
        'pg_dump',
        '-U', 'postgres',
        '-d', 'test_db',
        '-f', 'test_backup.sql'
    ], check=True)
    
    # Drop and recreate database
    with connection.cursor() as cursor:
        cursor.execute('DROP SCHEMA public CASCADE;')
        cursor.execute('CREATE SCHEMA public;')
    
    # Restore
    subprocess.run([
        'psql',
        '-U', 'postgres',
        '-d', 'test_db',
        '-f', 'test_backup.sql'
    ], check=True)
    
    # Check data restored
    assert User.objects.filter(email='user@example.com').exists()
```

================================================================================
## CHECKLIST
================================================================================

DATABASE TESTING CHECKLIST:
────────────────────────────────────────────────────────────────────────────
☐ Schema is correct
☐ Tables exist
☐ Columns have correct types
☐ Indexes exist
☐ Foreign keys work
☐ Cascade deletes work
☐ Unique constraints enforced
☐ Not null constraints enforced
☐ Check constraints enforced
☐ Queries return correct data
☐ Queries use indexes
☐ No N+1 query problems
☐ Migrations apply cleanly
☐ Migrations are reversible
☐ Transactions work correctly
☐ Data validation works
☐ No orphaned records
☐ Backup and restore work
☐ Performance is acceptable

================================================================================
## REMEMBER
================================================================================

✓ Test schema structure
✓ Test relationships
✓ Test constraints
✓ Test queries
✓ Test performance
✓ Test migrations
✓ Test transactions
✓ Test data integrity
✓ Use transactions in tests
✓ Clean up test data

Database integrity is critical!
================================================================================

