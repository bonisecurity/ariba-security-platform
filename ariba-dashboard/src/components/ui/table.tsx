/*
  Table component for Ariba Security Platform Dashboard
*/

import { cn } from "@/lib/utils";

interface TableHeaderProps {
  children: React.ReactNode;
  className?: string;
}

export function TableHeader({ children, className }: TableHeaderProps) {
  return (
    <th className={cn(
      "px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
      className
    )}>
      {children}
    </th>
  );
}

interface TableRowProps {
  children: React.ReactNode;
  className?: string;
}

export function TableRow({ children, className }: TableRowProps) {
  return (
    <tr className={cn(
      "hover:bg-gray-50 dark:hover:bg-gray-700",
      className
    )}>
      {children}
    </tr>
  );
}

interface TableCellProps {
  children: React.ReactNode;
  className?: string;
}

export function TableCell({ children, className }: TableCellProps) {
  return (
    <td className={cn(
      "px-6 py-4 whitespace-nowrap text-sm text-gray-500",
      className
    )}>
      {children}
    </td>
  );
}