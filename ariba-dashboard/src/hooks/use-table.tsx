/*
  Custom hook for table data fetching
*/

import { useState, useEffect } from "react";

type ColumnDef = {
  key: string;
  header: string;
};

type TableData = {
  endpoint: string;
  columns: string[];
};

export function useTable({ endpoint, columns }: TableData) {
  const [data, setData] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      try {
        const res = await fetch(endpoint, {
          headers: {
            "Content-Type": "application/json",
          },
        });
        const result = await res.json();
        setData(result || []);
      } catch (error) {
        console.error("Failed to fetch table data:", error);
        setData([]);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [endpoint]);

  return { data, isLoading };
}