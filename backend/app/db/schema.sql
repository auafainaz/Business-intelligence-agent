CREATE TABLE IF NOT EXISTS call_sessions (
    id TEXT PRIMARY KEY,
    twilio_call_sid TEXT UNIQUE,
    caller_number TEXT,
    called_number TEXT,
    session_status TEXT NOT NULL DEFAULT 'started',
    voice_model TEXT,
    transcript_status TEXT NOT NULL DEFAULT 'pending',
    started_at TEXT NOT NULL,
    ended_at TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transcripts (
    id TEXT PRIMARY KEY,
    call_session_id TEXT,
    raw_transcript TEXT NOT NULL,
    summary TEXT,
    extracted_fields_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (call_session_id) REFERENCES call_sessions(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS client_profiles (
    id TEXT PRIMARY KEY,
    call_session_id TEXT,
    full_name TEXT,
    role TEXT,
    email TEXT,
    phone TEXT,
    company_name TEXT NOT NULL,
    website TEXT,
    city_or_location TEXT,
    years_in_business INTEGER,
    number_of_locations INTEGER,
    business_type TEXT,
    industry TEXT,
    service_summary TEXT,
    company_summary TEXT,
    key_frustrations_json TEXT NOT NULL DEFAULT '[]',
    key_goals_json TEXT NOT NULL DEFAULT '[]',
    ai_familiarity TEXT,
    current_systems_json TEXT NOT NULL DEFAULT '[]',
    lead_source TEXT NOT NULL DEFAULT 'inbound_call',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (call_session_id) REFERENCES call_sessions(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS dashboard_payloads (
    id TEXT PRIMARY KEY,
    client_profile_id TEXT,
    call_session_id TEXT,
    dashboard_slug TEXT NOT NULL UNIQUE,
    public_payload_json TEXT NOT NULL,
    internal_payload_json TEXT NOT NULL,
    conversation_summary TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_profile_id) REFERENCES client_profiles(id) ON DELETE SET NULL,
    FOREIGN KEY (call_session_id) REFERENCES call_sessions(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_call_sessions_twilio_sid ON call_sessions(twilio_call_sid);
CREATE INDEX IF NOT EXISTS idx_client_profiles_email ON client_profiles(email);
CREATE INDEX IF NOT EXISTS idx_dashboard_payloads_slug ON dashboard_payloads(dashboard_slug);

CREATE TABLE IF NOT EXISTS automation_events (
    id TEXT PRIMARY KEY,
    dashboard_payload_id TEXT,
    dashboard_slug TEXT NOT NULL,
    event_type TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    request_json TEXT NOT NULL DEFAULT '{}',
    response_json TEXT NOT NULL DEFAULT '{}',
    error TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dashboard_payload_id) REFERENCES dashboard_payloads(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS delivery_records (
    id TEXT PRIMARY KEY,
    dashboard_payload_id TEXT,
    dashboard_slug TEXT NOT NULL,
    channel TEXT NOT NULL,
    recipient TEXT,
    status TEXT NOT NULL DEFAULT 'pending',
    provider_message_id TEXT,
    error TEXT,
    idempotency_key TEXT NOT NULL UNIQUE,
    sent_at TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dashboard_payload_id) REFERENCES dashboard_payloads(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_delivery_records_slug ON delivery_records(dashboard_slug);
CREATE INDEX IF NOT EXISTS idx_delivery_records_idempotency ON delivery_records(idempotency_key);
CREATE INDEX IF NOT EXISTS idx_automation_events_slug ON automation_events(dashboard_slug);
