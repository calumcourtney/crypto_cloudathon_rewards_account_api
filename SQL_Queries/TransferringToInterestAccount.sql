	DO $$
	DECLARE chain_id_var VARCHAR ( 255 );
	DECLARE user_id_var VARCHAR ( 255 );
	DECLARE interest_transactions_id_var VARCHAR ( 255 );
	DECLARE quantity_var DOUBLE PRECISION;
	
	DECLARE interest_account_supported_coins_id_var VARCHAR ( 255 );
	DECLARE interest_account_id_var VARCHAR ( 255 );
	DECLARE updatedQuantity_var DOUBLE PRECISION;
	BEGIN
	  -- THE BELOW VALUES SHOULD BE PARAMETERS AND DYNAMICALLY SET	  
	  chain_id_var := '{ChainID}';
	  user_id_var := '{UserID}';
	  quantity_var := {Quantity};
      interest_transactions_id_var := '{InterestTransactionsId}';
	  
	  
	  -- Based on the user and the crypo currency retrieveing the ID of the interest account
	  interest_account_id_var := (select interest_account.interest_account_id from interest_account
	  INNER JOIN users ON interest_account.user_id=users.user_id
	  INNER JOIN interest_account_supported_coins ON interest_account.interest_account_supported_coins_id=interest_account_supported_coins.interest_account_supported_coins_id
	  INNER JOIN supported_chains ON interest_account_supported_coins.chain_id=supported_chains.chain_id
	  where supported_chains.chain_id = chain_id_var and users.user_id = user_id_var);
	  RAISE NOTICE 'TEST2';
	  -- If the user doesn't have a interest account for this currency. We are creating one and setting the value to the transferred coins
	  if interest_account_id_var IS NULL then
		  interest_account_id_var := '{InterestAccountID}';
		  interest_account_supported_coins_id_var := (select interest_account_supported_coins_id from interest_account_supported_coins where chain_id = chain_id_var);
		  INSERT INTO interest_account(interest_account_id, user_id, interest_account_supported_coins_id, quantity, status, opened_date)
		  VALUES (interest_account_id_var, user_id_var, interest_account_supported_coins_id_var, quantity_var, 'OPEN', NOW())
		  RETURNING interest_account_id INTO interest_account_id_var;
		  updatedQuantity_var := quantity_var;
		  
	  -- If the user does have and interest account we are updating the value
	  else
		UPDATE interest_account SET quantity = quantity + quantity_var WHERE interest_account_id = interest_account_id_var;
		updatedQuantity_var := (select quantity from interest_account WHERE interest_account_id = interest_account_id_var);
	  end if;
	  RAISE NOTICE '>>>%<<<', updatedQuantity_var;
	  
	  -- Adding the transaction
	  
	  insert into interest_transactions(interest_transactions_id, interest_account_id, date, quantity, start_quantity, end_quantity)
	  VALUES (interest_transactions_id_var,interest_account_id_var,NOW(),quantity_var,updatedQuantity_var - quantity_var,updatedQuantity_var);	 
	  
	END;
	$$;