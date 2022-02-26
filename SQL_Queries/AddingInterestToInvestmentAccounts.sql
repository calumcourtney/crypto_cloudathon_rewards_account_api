do $$
declare interest_account record;
declare interestAccountID VARCHAR ( 255 );
declare interestRate DOUBLE PRECISION;
declare originalQuantity DOUBLE PRECISION;
declare updatedQuantity DOUBLE PRECISION;
declare interest_transactions_id_var VARCHAR ( 255 );
begin
    for interest_account in (select interest_account_id, interest_account_supported_coins_id, quantity from interest_account)
    loop 
		interestAccountID := interest_account.interest_account_id;
		interestRate := (select interest_rate from interest_account_supported_coins where interest_account_supported_coins_id=interest_account.interest_account_supported_coins_id);
		originalQuantity = interest_account.quantity;
		updatedQuantity = interest_account.quantity * interestRate;
		UPDATE interest_account SET quantity = updatedQuantity WHERE interest_account_id = interestAccountID;
		
		
		interest_transactions_id_var := (SELECT uuid_in(md5(random()::text || clock_timestamp()::text)::cstring));
		insert into interest_transactions(interest_transactions_id, interest_account_id, date, quantity, start_quantity, end_quantity)
	    VALUES (interest_transactions_id_var, interestAccountID,NOW(),updatedQuantity - originalQuantity,originalQuantity,updatedQuantity);
    end loop;
end;
$$;