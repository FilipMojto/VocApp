import { createContext, useContext, useState, type ReactNode } from "react";

type AuthMode = "login" | "register" | "idle";

interface AuthContextType {
  user: any;
  setUser: (user: any) => void;
  mode: AuthMode;
  setMode: (mode: AuthMode) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<any>(null);
  const [mode, setMode] = useState<AuthMode>("idle");

  return (
    <AuthContext.Provider value={{ user, setUser, mode, setMode }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
  return ctx;
}