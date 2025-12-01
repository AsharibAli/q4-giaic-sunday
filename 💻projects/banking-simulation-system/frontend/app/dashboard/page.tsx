"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Link from "next/link";

const DashboardPage = () => {
  const accounts = [
    { name: "Checking", balance: "1,234.56", currency: "USD" },
    { name: "Savings", balance: "5,678.90", currency: "USD" },
  ];

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Welcome to your Dashboard</h1>
      <div className="grid gap-6 md:grid-cols-2">
        {accounts.map((account) => (
          <Card key={account.name}>
            <CardHeader>
              <CardTitle>{account.name}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-2xl font-bold">${account.balance}</p>
              <p className="text-sm text-gray-500">{account.currency}</p>
            </CardContent>
          </Card>
        ))}
      </div>
      <div className="mt-6 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Link href="/dashboard/transactions">
          <Button className="w-full">View Transactions</Button>
        </Link>
        <Link href="/dashboard/transfer">
          <Button className="w-full">Transfer</Button>
        </Link>
        <Link href="/dashboard/deposit">
          <Button className="w-full">Deposit</Button>
        </Link>
        <Link href="/dashboard/withdraw">
          <Button className="w-full">Withdraw</Button>
        </Link>
      </div>
    </div>
  );
};

export default DashboardPage;
