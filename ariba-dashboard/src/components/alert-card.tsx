/*
  Alert Card component for Ariba Security Platform Dashboard
*/

import { Card, CardHeader, CardContent } from "@/components/ui/card";

export interface AlertCardProps {
  className?: string;
}

export function AlertCard({ className }: AlertCardProps) {
  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex justify-between items-start">
          <span />
          <span className="text-xs text-gray-500" />
        </div>
      </CardHeader>
      <CardContent>
        <p className="text-sm">{/* Alert content */}</p>
      </CardContent>
    </Card>
  );
}