import { useState } from "react";
import { Button, FormControl, FormLabel, Input, VStack } from "@chakra-ui/react";
import axios from "axios";

const Transaction = ({ user_id }) => {
  const [coinName, setCoinName] = useState("");
  const [amount, setAmount] = useState("");

  const handleAddTransaction = async () => {
    try {
      const response = await axios.post(`/${user_id}/transactions/add_transaction`, {
        coin_name: coinName,
        amount: amount,
      });
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const handleRemoveTransaction = async () => {
    try {
      const response = await axios.post(`/${user_id}/transactions/remove_transaction`, {
        coin_name: coinName,
        amount: amount,
      });
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <VStack spacing={4} align="start">
      <FormControl>
        <FormLabel>Coin Name</FormLabel>
        <Input value={coinName} onChange={(e) => setCoinName(e.target.value)} />
      </FormControl>
      <FormControl>
        <FormLabel>Amount</FormLabel>
        <Input value={amount} onChange={(e) => setAmount(e.target.value)} />
      </FormControl>
      <Button colorScheme="green" onClick={handleAddTransaction}>
        Buy/Add
      </Button>
      <Button colorScheme="red" onClick={handleRemoveTransaction}>
        Sell/Remove
      </Button>
    </VStack>
  );
};

export default Transaction;
