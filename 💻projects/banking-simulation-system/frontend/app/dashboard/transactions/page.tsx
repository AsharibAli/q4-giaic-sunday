"use client";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

const transactions = [
  {
    date: "2024-07-26",
    type: "Deposit",
    amount: "1,000.00",
    balance: "1,234.56",
  },
  {
    date: "2024-07-25",
    type: "Withdrawal",
    amount: "200.00",
    balance: "234.56",
  },
  {
    date: "2024-07-24",
    type: "Transfer",
    amount: "500.00",
    balance: "434.56",
  },
];

const TransactionsPage = () => {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Transactions</h1>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Date</TableHead>
            <TableHead>Type</TableHead>
            <TableHead className="text-right">Amount</TableHead>
            <TableHead className="text-right">Balance</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {transactions.map((transaction, index) => (
            <TableRow key={index}>
              <TableCell>{transaction.date}</TableCell>
              <TableCell>{transaction.type}</TableCell>
              <TableCell className="text-right">${transaction.amount}</TableCell>
              <TableCell className="text-right">${transaction.balance}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};

export default TransactionsPage;
