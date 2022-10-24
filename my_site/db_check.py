from authenticate.models import Vehicle

def db_check(plate_nr):

    

    cursor = connection.cursor()

    # Data modifying operation - commit required
    #cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
    #transaction.commit_unless_managed()
    
    # Data retrieval operation - no commit required
    cursor.execute("SELECT vehicle_id FROM authenticate.vehicle")
    row = cursor.fetchone()

    return row
