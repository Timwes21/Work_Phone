const tokenName: string = "workNumberToken";

export const getToken = (): string => {
    const token = localStorage.getItem(tokenName);
    return token? token: "noToken";
}

export const setToken = (token: string) => {
    localStorage.setItem(tokenName, token)
}