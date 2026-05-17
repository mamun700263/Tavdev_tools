import { create } from "zustand";
import { setToken, removeToken } from "@/lib/auth";

interface Account {
  id: string;
  email: string;
  role: string;
  is_verified: boolean;
  status: string;
}

interface AuthState {
  account: Account | null;
  isAuthenticated: boolean;
  login: (account: Account, accessToken: string, refreshToken: string) => void;
  logout: () => void;
  setAccount: (account: Account) => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  account: null,
  isAuthenticated: false,

  login: (account, accessToken, refreshToken) => {
    setToken(accessToken);
    localStorage.setItem("refresh_token", refreshToken);
    set({ account, isAuthenticated: true });
  },

  logout: () => {
    removeToken();
    localStorage.removeItem("refresh_token");
    set({ account: null, isAuthenticated: false });
  },

  setAccount: (account) => set({ account }),
}));