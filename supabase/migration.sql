-- Enable UUID generation if not already enabled
create extension if not exists pgcrypto;

create table if not exists customer (
    id uuid primary key default gen_random_uuid(),
    name text not null,
    email text not null unique,
    movies jsonb not null default '[]'::jsonb,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

-- `create table if not exists` does not add columns to an existing table.
-- These statements make the migration safe for databases created before the
-- customer registration fields were introduced.
alter table customer add column if not exists name text;
alter table customer add column if not exists email text;
alter table customer add column if not exists movies jsonb;
alter table customer add column if not exists created_at timestamptz;
alter table customer add column if not exists updated_at timestamptz;

alter table customer alter column movies set default '[]'::jsonb;
alter table customer alter column created_at set default now();
alter table customer alter column updated_at set default now();

update customer set movies = '[]'::jsonb where movies is null;
update customer set created_at = now() where created_at is null;
update customer set updated_at = now() where updated_at is null;

alter table customer alter column name set not null;
alter table customer alter column email set not null;
alter table customer alter column movies set not null;
alter table customer alter column created_at set not null;
alter table customer alter column updated_at set not null;

create unique index if not exists customer_email_key on customer (email);

-- Keep updated_at fresh on every row update
create or replace function set_updated_at()
returns trigger as $$
begin
    new.updated_at = now();
    return new;
end;
$$ language plpgsql;

drop trigger if exists trg_customer_updated_at on customer;

create trigger trg_customer_updated_at
before update on customer
for each row
execute function set_updated_at();
