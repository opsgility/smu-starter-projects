CREATE TYPE "public"."account_type" AS ENUM('taxable', 'traditional_ira', 'roth_ira', 'traditional_401k', 'roth_401k', 'hsa', 'cash');--> statement-breakpoint
CREATE TYPE "public"."asset_class" AS ENUM('us_equity', 'intl_equity', 'us_bond', 'intl_bond', 'reit', 'cash_equivalent', 'commodity', 'other');--> statement-breakpoint
CREATE TABLE IF NOT EXISTS "accounts" (
	"id" serial PRIMARY KEY NOT NULL,
	"user_id" integer NOT NULL,
	"name" text NOT NULL,
	"type" "account_type" NOT NULL,
	"institution" text,
	"is_active" boolean DEFAULT true NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS "holdings" (
	"id" serial PRIMARY KEY NOT NULL,
	"account_id" integer NOT NULL,
	"symbol" text NOT NULL,
	"name" text,
	"asset_class" "asset_class" NOT NULL,
	"quantity" numeric(18, 6) NOT NULL,
	"cost_basis" numeric(18, 2) NOT NULL,
	"acquired_at" timestamp NOT NULL,
	"notes" text
);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS "quote_cache" (
	"symbol" text PRIMARY KEY NOT NULL,
	"price" numeric(18, 4) NOT NULL,
	"change_pct" numeric(8, 4),
	"fetched_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS "users" (
	"id" serial PRIMARY KEY NOT NULL,
	"email" text NOT NULL,
	"birth_year" integer NOT NULL,
	"retirement_age" integer DEFAULT 65 NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	CONSTRAINT "users_email_unique" UNIQUE("email")
);
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "accounts" ADD CONSTRAINT "accounts_user_id_users_id_fk" FOREIGN KEY ("user_id") REFERENCES "public"."users"("id") ON DELETE no action ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "holdings" ADD CONSTRAINT "holdings_account_id_accounts_id_fk" FOREIGN KEY ("account_id") REFERENCES "public"."accounts"("id") ON DELETE cascade ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS "accounts_user_idx" ON "accounts" USING btree ("user_id");--> statement-breakpoint
CREATE INDEX IF NOT EXISTS "holdings_account_idx" ON "holdings" USING btree ("account_id");--> statement-breakpoint
CREATE INDEX IF NOT EXISTS "holdings_symbol_idx" ON "holdings" USING btree ("symbol");