"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const AccountsPage = () => {
  const accounts = [
    {
      name: "Checking",
      accountNumber: "**** **** **** 1234",
      balance: "1,234.56",
      currency: "USD",
    },
    {
      name: "Savings",
      accountNumber: "**** **** **** 5678",
      balance: "5,678.90",
      currency: "USD",
    },
  ];

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Accounts</h1>
      <div className="grid gap-6 md:grid-cols-2">
        {accounts.map((account) => (
          <Card key={account.name}>
            <CardHeader>
              <CardTitle>{account.name}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-500">{account.accountNumber}</p>
              <p className="text-2xl font-bold">${account.balance}</p>
              <p className="text-sm text-gray-500">{account.currency}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default AccountsPage;
