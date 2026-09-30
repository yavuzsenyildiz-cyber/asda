import Foundation

class PCViewModel: ObservableObject {
  @Published var device: Device?
  @Published var backendURL = "http://localhost:3000"
  @Published var token: String?

  private let userDefaults = UserDefaults.standard
  private let tokenKey = "auth_token"
  private let deviceIdKey = "device_id"

  init() {
    self.token = userDefaults.string(forKey: tokenKey)
    if let savedURL = userDefaults.string(forKey: "backend_url") {
      self.backendURL = savedURL
    }
  }

  func login(deviceId: String, completion: @escaping (Bool, String?) -> Void) {
    let url = URL(string: "\(backendURL)/api/auth/login")!
    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    request.setValue("application/json", forHTTPHeaderField: "Content-Type")

    let body = ["deviceId": deviceId]
    request.httpBody = try? JSONSerialization.data(withJSONObject: body)

    URLSession.shared.dataTask(with: request) { [weak self] data, _, error in
      DispatchQueue.main.async {
        if let error = error {
          completion(false, error.localizedDescription)
          return
        }

        guard let data = data else {
          completion(false, "Veri alınamadı")
          return
        }

        do {
          let response = try JSONDecoder().decode(LoginResponse.self, from: data)
          self?.token = response.token
          self?.device = response.device
          self?.userDefaults.set(response.token, forKey: self?.tokenKey ?? "")
          self?.userDefaults.set(deviceId, forKey: self?.deviceIdKey ?? "")
          completion(true, nil)
        } catch {
          completion(false, "Hata: \(error.localizedDescription)")
        }
      }
    }.resume()
  }

  func powerOnPC(completion: @escaping (Bool, String?) -> Void) {
    guard let token = token else {
      completion(false, "Token bulunamadı")
      return
    }

    let url = URL(string: "\(backendURL)/api/device/power-on")!
    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    request.setValue("application/json", forHTTPHeaderField: "Content-Type")
    request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")

    URLSession.shared.dataTask(with: request) { data, _, error in
      DispatchQueue.main.async {
        if let error = error {
          completion(false, "Hata: \(error.localizedDescription)")
          return
        }

        guard let data = data else {
          completion(false, "Veri alınamadı")
          return
        }

        do {
          let response = try JSONDecoder().decode(PowerOnResponse.self, from: data)
          completion(true, response.message)
        } catch {
          completion(false, "Hata: \(error.localizedDescription)")
        }
      }
    }.resume()
  }

  func logout() {
    token = nil
    device = nil
    userDefaults.removeObject(forKey: tokenKey)
    userDefaults.removeObject(forKey: deviceIdKey)
  }
}

struct Device: Codable {
  let id: String
  let deviceName: String
  let macAddress: String
  let createdAt: String
}

struct LoginResponse: Codable {
  let token: String
  let device: Device
}

struct PowerOnResponse: Codable {
  let commandId: String
  let status: String
  let message: String
}
