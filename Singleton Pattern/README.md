# Singleton Pattern (Design Pattern) — English & বাংলা

## Table of Contents
- [1) What is the Singleton Pattern?](#1-what-is-the-singleton-pattern)
- [2) When should you use it?](#2-when-should-you-use-it)
- [3) When should you avoid it? (Common problems)](#3-when-should-you-avoid-it-common-problems)
- [4) Core rules of a good Singleton](#4-core-rules-of-a-good-singleton)
- [5) Implementations (with code)](#5-implementations-with-code)
  - [5.1 Java: Eager initialization](#51-java-eager-initialization)
  - [5.2 Java: Lazy (not thread-safe)](#52-java-lazy-not-thread-safe)
  - [5.3 Java: Thread-safe lazy (synchronized)](#53-java-thread-safe-lazy-synchronized)
  - [5.4 Java: Double-checked locking (volatile)](#54-java-double-checked-locking-volatile)
  - [5.5 Java: Initialization-on-demand holder idiom](#55-java-initialization-on-demand-holder-idiom)
  - [5.6 Java: Enum singleton (recommended)](#56-java-enum-singleton-recommended)
  - [5.7 Python: Module + class approaches](#57-python-module--class-approaches)
  - [5.8 C#: Lazy<T> singleton](#58-c-lazyt-singleton)
- [6) Realistic example: App configuration](#6-realistic-example-app-configuration)
- [7) Singleton vs Dependency Injection (DI)](#7-singleton-vs-dependency-injection-di)
- [8) Quick checklist](#8-quick-checklist)

---

## Repo resources (PDF)

### English
This repository also contains reference PDFs inside `Singleton Pattern/`:
- `Singleton Pattern/Singleton Pattern (Design Pattern).pdf`
- `Singleton Pattern/Singleton Assignment.pdf`

### বাংলা
এই রিপোজিটরিতে `Singleton Pattern/` ফোল্ডারের ভেতরে কিছু রেফারেন্স PDF আছে:
- `Singleton Pattern/Singleton Pattern (Design Pattern).pdf`
- `Singleton Pattern/Singleton Assignment.pdf`

---

## 1) What is the Singleton Pattern?

### English
The **Singleton** pattern ensures that a class has **exactly one instance** in your application and provides a **global access point** to it.

Think of it like:
- One “shared” object (e.g., logger/config/cache) that everyone uses.
- You don’t want multiple copies because that causes duplicated state, extra memory usage, or inconsistent behavior.

**Classic structure**
- Private constructor → prevents `new`.
- Private static field → stores the single instance.
- Public static method → returns the instance (often named `getInstance()`).

### বাংলা
**Singleton** প্যাটার্ন নিশ্চিত করে যে একটি ক্লাসের **মাত্র একটি instance** থাকবে এবং সেটিতে অ্যাপ্লিকেশনের যেকোন জায়গা থেকে **global access** পাওয়া যাবে।

সহজভাবে ভাবুন:
- একটি “shared” অবজেক্ট (যেমন logger/config/cache) যেটা সবাই ব্যবহার করবে।
- একাধিক কপি হলে state ডুপ্লিকেট, মেমোরি বেশি খরচ, বা inconsistent behavior হতে পারে।

**ক্লাসিক স্ট্রাকচার**
- Private constructor → `new` করা বন্ধ করে।
- Private static ফিল্ড → একটাই instance ধরে রাখে।
- Public static মেথড → instance রিটার্ন করে (সাধারণত `getInstance()`).

---

## 2) When should you use it?

### English
Singleton is useful when:
- There must be **one** “source of truth” (e.g., `AppConfig`).
- You want a single shared resource (e.g., connection pool, cache).
- You need a single coordinator (e.g., metrics registry, feature flags).

Examples:
- Logging service (one log pipeline)
- Configuration loader (read once, use everywhere)
- In-memory cache (shared by all modules)

### বাংলা
Singleton ভালো কাজ করে যখন:
- “source of truth” **একটাই** থাকা দরকার (যেমন `AppConfig`)।
- একটি shared resource একবারই তৈরি করে সবাইকে ব্যবহার করাতে চান (যেমন connection pool, cache)।
- একটাই coordinator দরকার (যেমন metrics registry, feature flags)।

উদাহরণ:
- Logger (একটাই log pipeline)
- Configuration loader (একবার লোড, সর্বত্র ব্যবহার)
- In-memory cache (সব মডিউল শেয়ার করে)

---

## 3) When should you avoid it? (Common problems)

### English
Singleton is often criticized because it can behave like a **global variable**:
- **Hidden dependencies:** a class silently depends on the singleton.
- **Hard to test:** tests share state; order-dependent failures happen.
- **Tight coupling:** replacing implementation becomes harder.
- **Concurrency hazards:** naive lazy singletons break under threads.

Avoid Singleton when:
- You can pass dependencies explicitly (constructor params).
- You are building large systems where testability matters a lot.
- You need multiple instances for different contexts (multi-tenant, multi-env).

### বাংলা
Singleton অনেক সময় **global variable** এর মতো সমস্যা তৈরি করে:
- **Hidden dependency:** কোন ক্লাস সাইলেন্টলি singleton-এর ওপর নির্ভর করে।
- **Test করা কঠিন:** টেস্টগুলো একই state শেয়ার করে; order-dependent bug হয়।
- **Tight coupling:** implementation বদলানো কঠিন হয়।
- **Concurrency সমস্যা:** থ্রেডে naive lazy singleton ভেঙে যেতে পারে।

Singleton এড়িয়ে চলুন যখন:
- Dependency constructor দিয়ে pass করা যায়।
- বড় সিস্টেমে testability খুব গুরুত্বপূর্ণ।
- আলাদা context-এর জন্য একাধিক instance দরকার (multi-tenant/multi-env)।

---

## 4) Core rules of a good Singleton

### English
To implement correctly, think about these rules:
1. **Single instance**: you never create more than one.
2. **Controlled creation**: clients cannot use `new`.
3. **Thread safety** (if your app is multi-threaded).
4. **Serialization/reflection safety** (Java-specific concerns).
5. **Clear lifecycle**: know when it’s created and how it’s reset (if ever).

### বাংলা
সঠিক Singleton বানাতে সাধারণত এগুলো নিশ্চিত করতে হয়:
1. **একটাই instance**: কখনো একাধিক তৈরি হবে না।
2. **Creation control**: বাইরে থেকে `new` করা যাবে না।
3. **Thread safety** (যদি অ্যাপ multi-threaded হয়)।
4. **Serialization/reflection safety** (Java-তে গুরুত্বপূর্ণ)।
5. **Lifecycle পরিষ্কার**: কখন তৈরি হবে, দরকার হলে reset হবে কিনা।

---

## 5) Implementations (with code)

> Note: Pick one approach per language/project. Don’t mix multiple singleton styles unless there’s a strong reason.

### 5.1 Java: Eager initialization

### English
Creates the instance when the class loads. Simple and thread-safe.
```java
public final class EagerSingleton {
  private static final EagerSingleton INSTANCE = new EagerSingleton();

  private EagerSingleton() {}

  public static EagerSingleton getInstance() {
    return INSTANCE;
  }
}
```

### বাংলা
ক্লাস লোড হওয়ার সময়ই instance তৈরি হয়। Simple এবং thread-safe.
```java
public final class EagerSingleton {
  private static final EagerSingleton INSTANCE = new EagerSingleton();

  private EagerSingleton() {}

  public static EagerSingleton getInstance() {
    return INSTANCE;
  }
}
```

---

### 5.2 Java: Lazy (not thread-safe)

### English
Creates the instance only when first needed, but **breaks in multi-threading**.
```java
public final class LazySingletonUnsafe {
  private static LazySingletonUnsafe instance;

  private LazySingletonUnsafe() {}

  public static LazySingletonUnsafe getInstance() {
    if (instance == null) {
      instance = new LazySingletonUnsafe();
    }
    return instance;
  }
}
```

### বাংলা
প্রথমবার দরকার হলে instance তৈরি হয়, কিন্তু **multi-threading এ ভেঙে যায়**।
```java
public final class LazySingletonUnsafe {
  private static LazySingletonUnsafe instance;

  private LazySingletonUnsafe() {}

  public static LazySingletonUnsafe getInstance() {
    if (instance == null) {
      instance = new LazySingletonUnsafe();
    }
    return instance;
  }
}
```

---

### 5.3 Java: Thread-safe lazy (synchronized)

### English
Thread-safe but slower because every call locks.
```java
public final class LazySingletonSynchronized {
  private static LazySingletonSynchronized instance;

  private LazySingletonSynchronized() {}

  public static synchronized LazySingletonSynchronized getInstance() {
    if (instance == null) {
      instance = new LazySingletonSynchronized();
    }
    return instance;
  }
}
```

### বাংলা
Thread-safe, কিন্তু প্রতিবার কল করলে lock হওয়ায় ধীর হতে পারে।
```java
public final class LazySingletonSynchronized {
  private static LazySingletonSynchronized instance;

  private LazySingletonSynchronized() {}

  public static synchronized LazySingletonSynchronized getInstance() {
    if (instance == null) {
      instance = new LazySingletonSynchronized();
    }
    return instance;
  }
}
```

---

### 5.4 Java: Double-checked locking (volatile)

### English
Avoids locking after initialization. Must use `volatile`.
```java
public final class SingletonDCL {
  private static volatile SingletonDCL instance;

  private SingletonDCL() {}

  public static SingletonDCL getInstance() {
    if (instance == null) {
      synchronized (SingletonDCL.class) {
        if (instance == null) {
          instance = new SingletonDCL();
        }
      }
    }
    return instance;
  }
}
```

### বাংলা
Initialization হয়ে গেলে আর lock লাগে না। `volatile` ব্যবহার করা জরুরি।
```java
public final class SingletonDCL {
  private static volatile SingletonDCL instance;

  private SingletonDCL() {}

  public static SingletonDCL getInstance() {
    if (instance == null) {
      synchronized (SingletonDCL.class) {
        if (instance == null) {
          instance = new SingletonDCL();
        }
      }
    }
    return instance;
  }
}
```

---

### 5.5 Java: Initialization-on-demand holder idiom

### English
Clean, lazy, and thread-safe using class loading.
```java
public final class HolderSingleton {
  private HolderSingleton() {}

  private static final class Holder {
    private static final HolderSingleton INSTANCE = new HolderSingleton();
  }

  public static HolderSingleton getInstance() {
    return Holder.INSTANCE;
  }
}
```

### বাংলা
ক্লাস লোডিংয়ের সুবিধা নিয়ে clean lazy + thread-safe সমাধান।
```java
public final class HolderSingleton {
  private HolderSingleton() {}

  private static final class Holder {
    private static final HolderSingleton INSTANCE = new HolderSingleton();
  }

  public static HolderSingleton getInstance() {
    return Holder.INSTANCE;
  }
}
```

---

### 5.6 Java: Enum singleton (recommended)

### English
The most robust approach in Java (handles serialization safely and is thread-safe by design).
```java
public enum AppSettings {
  INSTANCE;

  private String mode = "prod";

  public String getMode() {
    return mode;
  }

  public void setMode(String mode) {
    this.mode = mode;
  }
}
```
Usage:
```java
AppSettings.INSTANCE.setMode("dev");
System.out.println(AppSettings.INSTANCE.getMode());
```

### বাংলা
Java-তে সবচেয়ে robust উপায় (serialization-safe, এবং thread-safe)।
```java
public enum AppSettings {
  INSTANCE;

  private String mode = "prod";

  public String getMode() {
    return mode;
  }

  public void setMode(String mode) {
    this.mode = mode;
  }
}
```
ব্যবহার:
```java
AppSettings.INSTANCE.setMode("dev");
System.out.println(AppSettings.INSTANCE.getMode());
```

---

### 5.7 Python: Module + class approaches

### English
In Python, a common “singleton” is simply a **module** (modules are imported once per process).

Option A: module-as-singleton
```python
# settings.py
mode = "prod"
```
Usage:
```python
import settings
settings.mode = "dev"
print(settings.mode)
```

Option B: class singleton with `__new__`
```python
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### বাংলা
Python-এ অনেক সময় **module**-ই singleton হিসেবে যথেষ্ট (প্রসেসে একবারই import হয়)।

Option A: module-as-singleton
```python
# settings.py
mode = "prod"
```
ব্যবহার:
```python
import settings
settings.mode = "dev"
print(settings.mode)
```

Option B: `__new__` ব্যবহার করে class singleton
```python
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

---

### 5.8 C#: Lazy<T> singleton

### English
Simple, thread-safe, lazy singleton.
```csharp
public sealed class AppConfig {
  private static readonly Lazy<AppConfig> Lazy =
    new Lazy<AppConfig>(() => new AppConfig());

  private AppConfig() {}

  public static AppConfig Instance => Lazy.Value;
}
```

### বাংলা
Simple, thread-safe, lazy singleton।
```csharp
public sealed class AppConfig {
  private static readonly Lazy<AppConfig> Lazy =
    new Lazy<AppConfig>(() => new AppConfig());

  private AppConfig() {}

  public static AppConfig Instance => Lazy.Value;
}
```

---

## 6) Realistic example: App configuration

### English
Problem: You want to load configuration once (from file/env/DB), then use it everywhere.

Design idea:
- `AppConfig` reads config once.
- Other services ask `AppConfig.getInstance()` (or DI injects it).

Typical fields:
- `baseUrl`, `dbConnectionString`, `featureFlags`, `logLevel`

### বাংলা
সমস্যা: কনফিগারেশন (file/env/DB) একবার লোড করে সর্বত্র ব্যবহার করতে চান।

ডিজাইন আইডিয়া:
- `AppConfig` একবার কনফিগ লোড করবে।
- অন্য সার্ভিসগুলো `AppConfig.getInstance()` দিয়ে নেবে (বা DI দিয়ে inject করা হবে)।

সাধারণ ফিল্ড:
- `baseUrl`, `dbConnectionString`, `featureFlags`, `logLevel`

---

## 7) Singleton vs Dependency Injection (DI)

### English
Many modern codebases prefer **Dependency Injection**:
- Easier to test (swap real object with mock/fake).
- Dependencies are explicit (constructor parameters).
- Lifecycle can be managed by the DI container (singleton scope, per-request scope, etc.).

Good rule:
- Use Singleton only when you truly need one instance and you can manage the trade-offs.
- Prefer DI when building larger, test-heavy applications.

### বাংলা
অনেক আধুনিক কোডবেসে **Dependency Injection** বেশি পছন্দ করা হয়:
- টেস্ট সহজ (real object এর বদলে mock/fake দেওয়া যায়)।
- dependency স্পষ্ট থাকে (constructor parameters)।
- DI container lifecycle handle করতে পারে (singleton scope, per-request scope ইত্যাদি)।

থাম্ব রুল:
- সত্যিই একটাই instance দরকার হলে Singleton ব্যবহার করুন এবং trade-off বুঝে নিন।
- বড়/টেস্ট-ভিত্তিক প্রজেক্টে DI প্রেফার করুন।

---

## 8) Quick checklist

### English
- Do you *really* need only one instance?
- Is the implementation thread-safe (if needed)?
- Is shared mutable state going to cause bugs?
- Will this make tests harder?
- Would DI (singleton scope) be a cleaner solution?

### বাংলা
- সত্যিই কি একটাই instance লাগবে?
- থ্রেড থাকলে implementation কি thread-safe?
- shared mutable state বাগ তৈরি করবে না তো?
- টেস্ট কঠিন হয়ে যাবে না তো?
- DI (singleton scope) কি আরও পরিষ্কার সমাধান?
