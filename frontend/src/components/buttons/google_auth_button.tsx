// components/GoogleLoginButton.tsx

export default function GoogleLoginButton() {
  const handleGoogleLogin = () => {
    window.location.href =
      `${process.env.NEXT_PUBLIC_API_URL}/accounts/auth/google/login`;
  };

  return (
    <button
      type="button"
      onClick={handleGoogleLogin}
        className="
        w-full
        border border-gray-300
        bg-white text-gray-700
        my-4 py-2
        rounded-lg
        text-sm font-medium
        flex items-center justify-center gap-2

        hover:bg-gray-100
        hover:border-gray-400
        hover:shadow-sm
        transition-all duration-150

        active:bg-gray-200
        "
    >
      <img
        src="/google.png"
        alt="Google"
        className="w-5 h-5"
      />
      Continue with Google
    </button>
  );
}