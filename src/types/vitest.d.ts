/**
 * Simple type declaration for vitest to avoid lint errors
 */
declare module 'vitest' {
  export function describe(name: string, fn: () => void): void;
  export function it(name: string, fn: () => void | Promise<void>): void;
  export function beforeEach(fn: () => void | Promise<void>): void;
  export function expect<T>(actual: T): {
    toBe(expected: T): void;
    toEqual(expected: any): void;
    toHaveBeenCalled(): void;
    toHaveBeenCalledTimes(times: number): void;
    toHaveBeenCalledWith(...args: any[]): void;
    toThrow(message?: string | RegExp): void;
    rejects: {
      toThrow(message?: string | RegExp): Promise<void>;
    };
  };
  export const vi: {
    fn: <T extends (...args: any[]) => any>(implementation?: T) => {
      (...args: Parameters<T>): ReturnType<T>;
      mockResolvedValue: (val: any) => any;
      mockResolvedValueOnce: (val: any) => any;
      mockRejectedValue: (val: any) => any;
      mockRejectedValueOnce: (val: any) => any;
      mockImplementation: (fn: T) => any;
      mockImplementationOnce: (fn: T) => any;
    };
    clearAllMocks: () => void;
    mock: (path: string, factory?: () => any) => void;
  };
}
