import duckdb
from mtfck.ingestion import update_to_today, get_connection

def sync_sequence():
    """Ensure stock_id_seq is consistent with stock_master.stock_id."""
    conn = get_connection()
    try:
        # Check if table exists
        conn.execute("SELECT 1 FROM stock_master LIMIT 1")
    except duckdb.CatalogException:
        return # Table doesn't exist yet, nothing to sync

    # Get Max ID
    row = conn.execute("SELECT MAX(stock_id) FROM stock_master").fetchone()
    max_id = row[0] if row and row[0] is not None else 0

    # Sync sequence
    print(f"Syncing sequence to ensure it is > {max_id}")
    try:
        seq_info = conn.execute("SELECT last_value FROM duckdb_sequences() WHERE sequence_name='stock_id_seq'").fetchone()
        if seq_info:
            current_val = seq_info[0] if seq_info[0] is not None else 0
            if current_val < max_id:
                diff = max_id - current_val
                print(f"Sequence lagging by {diff}. Fast-forwarding...")
                # We can loop, or use nextval in a loop in SQL
                conn.execute(f"SELECT nextval('stock_id_seq') FROM range({diff})")
                print(f"Sequence fast-forwarded to > {max_id}")
            else:
                print(f"Sequence is already at {current_val} (>= {max_id}). OK.")
        else:
            print("Sequence stock_id_seq not found in metadata.")

    except Exception as e:
        print(f"Warning: Could not sync sequence: {e}")

if __name__ == "__main__":
    sync_sequence()
    update_to_today()
