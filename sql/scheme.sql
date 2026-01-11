CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  phone TEXT UNIQUE NOT NULL,
  country TEXT,
  device_fingerprint TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE creators (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id),
  display_name TEXT,
  payout_phone TEXT,
  payout_method TEXT,
  country TEXT
);

CREATE TABLE events (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  creator_id UUID REFERENCES creators(id),
  title TEXT,
  venue TEXT,
  city TEXT,
  country TEXT,
  start_time TIMESTAMP,
  end_time TIMESTAMP,
  status TEXT
);

CREATE TABLE tickets (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  event_id UUID REFERENCES events(id),
  name TEXT,
  price NUMERIC,
  supply INT,
  resale_allowed BOOLEAN,
  royalty_percent INT
);

CREATE TABLE orders (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  event_id UUID REFERENCES events(id),
  amount NUMERIC,
  status TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE payments (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  order_id UUID REFERENCES orders(id),
  provider TEXT,
  provider_ref TEXT,
  phone TEXT,
  amount NUMERIC,
  status TEXT,
  raw_callback JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE passes (
  id UUID PRIMARY KEY,
  ticket_id UUID REFERENCES tickets(id),
  order_id UUID REFERENCES orders(id),
  owner_id UUID REFERENCES users(id),
  qr_hash TEXT UNIQUE,
  status TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE resales (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  pass_id UUID REFERENCES passes(id),
  seller_id UUID REFERENCES users(id),
  price NUMERIC,
  status TEXT
);

CREATE TABLE scans (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  pass_id UUID REFERENCES passes(id),
  scanner_id TEXT,
  scanned_at TIMESTAMP DEFAULT NOW(),
  result TEXT
);
