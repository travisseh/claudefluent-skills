---
name: supabase-postgres-best-practices
description: Postgres performance optimization and best practices from Supabase. Use this skill when writing, reviewing, or optimizing Postgres queries, schema designs, or database configurations.
license: MIT
metadata:
  author: supabase
  version: "1.0.0"
---

# Supabase Postgres Best Practices

Comprehensive performance optimization guide for Postgres, maintained by Supabase. Contains 30 rules across 8 categories, prioritized by impact to guide automated query optimization and schema design.

## When to Apply

Reference these guidelines when:
- Writing SQL queries or designing schemas
- Implementing indexes or query optimization
- Reviewing database performance issues
- Configuring connection pooling or scaling
- Optimizing for Postgres-specific features
- Working with Row-Level Security (RLS)

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Query Performance | CRITICAL | `query-` |
| 2 | Connection Management | CRITICAL | `conn-` |
| 3 | Security & RLS | CRITICAL | `security-` |
| 4 | Schema Design | HIGH | `schema-` |
| 5 | Concurrency & Locking | MEDIUM-HIGH | `lock-` |
| 6 | Data Access Patterns | MEDIUM | `data-` |
| 7 | Monitoring & Diagnostics | LOW-MEDIUM | `monitor-` |
| 8 | Advanced Features | LOW | `advanced-` |

## How to Use

Read individual rule files in `references/` for detailed explanations and SQL examples:

```
references/query-missing-indexes.md
references/schema-partitioning.md
references/security-rls-performance.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect SQL example with explanation
- Correct SQL example with explanation
- Optional EXPLAIN output or metrics
- Additional context and references
- Supabase-specific notes (when applicable)

---

## Rule Index

### 1. Query Performance (CRITICAL)

Slow queries, missing indexes, inefficient query plans. The most common source of Postgres performance issues.

| Rule | Impact | File |
|------|--------|------|
| Add Indexes on WHERE and JOIN Columns | CRITICAL (100-1000x faster) | `references/query-missing-indexes.md` |
| Choose the Right Index Type for Your Data | HIGH (10-100x improvement) | `references/query-index-types.md` |
| Create Composite Indexes for Multi-Column Queries | HIGH (5-10x faster) | `references/query-composite-indexes.md` |
| Use Covering Indexes to Avoid Table Lookups | MEDIUM-HIGH (2-5x faster) | `references/query-covering-indexes.md` |
| Use Partial Indexes for Filtered Queries | HIGH (5-20x smaller indexes) | `references/query-partial-indexes.md` |

### 2. Connection Management (CRITICAL)

Connection pooling, limits, and serverless strategies. Critical for applications with high concurrency or serverless deployments.

| Rule | Impact | File |
|------|--------|------|
| Configure Idle Connection Timeouts | HIGH (reclaim 30-50% slots) | `references/conn-idle-timeout.md` |
| Set Appropriate Connection Limits | CRITICAL (prevent crashes) | `references/conn-limits.md` |
| Use Connection Pooling for All Applications | CRITICAL (10-100x more users) | `references/conn-pooling.md` |
| Use Prepared Statements Correctly with Pooling | HIGH (avoid conflicts) | `references/conn-prepared-statements.md` |

### 3. Security & RLS (CRITICAL)

Row-level security, privilege management, and secure access patterns for multi-tenant applications.

| Rule | Impact | File |
|------|--------|------|
| Apply Principle of Least Privilege | CRITICAL (prevent breaches) | `references/security-privileges.md` |
| Enable Row Level Security for Multi-Tenant Data | CRITICAL (data isolation) | `references/security-rls-basics.md` |
| Optimize RLS Policies for Performance | HIGH (5-10x faster RLS) | `references/security-rls-performance.md` |

### 4. Schema Design (HIGH)

Data types, primary keys, partitioning, and naming conventions that affect long-term performance and maintainability.

| Rule | Impact | File |
|------|--------|------|
| Choose Appropriate Data Types | MEDIUM (20-40% storage reduction) | `references/schema-data-types.md` |
| Index Foreign Key Columns | HIGH (prevent full table locks) | `references/schema-foreign-key-indexes.md` |
| Partition Large Tables for Better Performance | HIGH (10-100x faster on large tables) | `references/schema-partitioning.md` |
| Select Optimal Primary Key Strategy | MEDIUM (affects insert perf) | `references/schema-primary-keys.md` |
| Use Lowercase Identifiers for Compatibility | LOW (prevents quoting issues) | `references/schema-lowercase-identifiers.md` |

### 5. Concurrency & Locking (MEDIUM-HIGH)

Transaction management, deadlock prevention, and lock optimization for concurrent workloads.

| Rule | Impact | File |
|------|--------|------|
| Keep Transactions Short to Reduce Lock Contention | HIGH (prevent timeouts) | `references/lock-short-transactions.md` |
| Prevent Deadlocks with Consistent Lock Ordering | MEDIUM-HIGH (eliminate deadlocks) | `references/lock-deadlock-prevention.md` |
| Use Advisory Locks for Application-Level Locking | MEDIUM (custom coordination) | `references/lock-advisory.md` |
| Use SKIP LOCKED for Non-Blocking Queue Processing | MEDIUM (lock-free queues) | `references/lock-skip-locked.md` |

### 6. Data Access Patterns (MEDIUM)

Batch operations, pagination strategies, and query patterns that reduce round-trips and improve throughput.

| Rule | Impact | File |
|------|--------|------|
| Batch INSERT Statements for Bulk Data | MEDIUM (10-50x faster inserts) | `references/data-batch-inserts.md` |
| Eliminate N+1 Queries with Batch Loading | HIGH (10-100x fewer queries) | `references/data-n-plus-one.md` |
| Use Cursor-Based Pagination Instead of OFFSET | MEDIUM-HIGH (consistent perf) | `references/data-pagination.md` |
| Use UPSERT for Insert-or-Update Operations | MEDIUM (atomic operations) | `references/data-upsert.md` |

### 7. Monitoring & Diagnostics (LOW-MEDIUM)

Query analysis, statistics maintenance, and performance monitoring tools.

| Rule | Impact | File |
|------|--------|------|
| Enable pg_stat_statements for Query Analysis | MEDIUM (find slow queries) | `references/monitor-pg-stat-statements.md` |
| Maintain Table Statistics with VACUUM and ANALYZE | MEDIUM (accurate plans) | `references/monitor-vacuum-analyze.md` |
| Use EXPLAIN ANALYZE to Diagnose Slow Queries | HIGH (identify bottlenecks) | `references/monitor-explain-analyze.md` |

### 8. Advanced Features (LOW)

JSONB indexing, full-text search, and other Postgres-specific capabilities.

| Rule | Impact | File |
|------|--------|------|
| Index JSONB Columns for Efficient Querying | MEDIUM (10-100x faster JSONB) | `references/advanced-jsonb-indexing.md` |
| Use tsvector for Full-Text Search | MEDIUM (100x faster than LIKE) | `references/advanced-full-text-search.md` |

---

## Quick Reference: Top 10 Rules by Impact

1. **Add indexes on WHERE/JOIN columns** - `references/query-missing-indexes.md` (100-1000x)
2. **Use connection pooling** - `references/conn-pooling.md` (10-100x more users)
3. **Set connection limits** - `references/conn-limits.md` (prevent crashes)
4. **Apply least privilege** - `references/security-privileges.md` (prevent breaches)
5. **Enable RLS for multi-tenant** - `references/security-rls-basics.md` (data isolation)
6. **Choose right index type** - `references/query-index-types.md` (10-100x)
7. **Eliminate N+1 queries** - `references/data-n-plus-one.md` (10-100x fewer queries)
8. **Partition large tables** - `references/schema-partitioning.md` (10-100x)
9. **Use partial indexes** - `references/query-partial-indexes.md` (5-20x)
10. **Optimize RLS policies** - `references/security-rls-performance.md` (5-10x)

---

## References

- https://www.postgresql.org/docs/current/
- https://supabase.com/docs
- https://wiki.postgresql.org/wiki/Performance_Optimization
- https://supabase.com/docs/guides/database/overview
- https://supabase.com/docs/guides/auth/row-level-security
