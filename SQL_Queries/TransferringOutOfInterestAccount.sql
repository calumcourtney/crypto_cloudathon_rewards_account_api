DO $$
DECLARE interest_account_id_var VARCHAR ( 255 );
DECLARE quantity_var DOUBLE PRECISION;
DECLARE updatedQuantity_var DOUBLE PRECISION;
declare interest_transactions_id_var VARCHAR ( 255 );

BEGIN
    quantity_var := {Quantity};
    interest_account_id_var := '{InterestAccountID}';
    UPDATE interest_account SET quantity = quantity - quantity_var WHERE interest_account_id = interest_account_id_var;
    updatedQuantity_var := (select quantity from interest_account WHERE interest_account_id = interest_account_id_var);
    
    interest_transactions_id_var := (SELECT uuid_in(md5(random()::text || clock_timestamp()::text)::cstring));
    insert into interest_transactions(interest_transactions_id, interest_account_id, date, quantity, start_quantity, end_quantity)
    VALUES (interest_transactions_id_var,interest_account_id_var,NOW(),quantity_var,updatedQuantity_var + quantity_var,updatedQuantity_var);
END;
$$;